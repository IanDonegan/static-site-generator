import re
from enum import Enum
from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered"
    ORDERED_LIST = "ordered"

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Text Type not recognized")
    props = {}
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            tag = None
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props["href"] = text_node.url
        case TextType.IMAGE:
            tag = "img"
            text = ""
            props["src"] = text_node.url
            props["alt"] = text_node.text
        case _:
            raise NotImplementedError("Text Type value recognized but not handled")
    return LeafNode(tag, text, props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            processed_nodes.append(node)
            continue
        elif delimiter in node.text:
            sections = node.text.split(delimiter)
            if len(sections) % 2 != 1:
                raise Exception("There must be an even number of delimeters")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 1:
                    type = text_type
                else:
                    type = TextType.TEXT
                processed_nodes.append(TextNode(sections[i], type))
        else:
            processed_nodes.append(node)
    return processed_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            processed_nodes.append(node)
            continue
        text = node.text
        matches = extract_markdown_images(node.text)
        for match in matches:
            split = text.split(f"![{match[0]}]({match[1]})")
            if split[0] != "":
                processed_nodes.append(TextNode(split[0], TextType.TEXT))
            processed_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = split[1]
        if len(matches) == 0:
            processed_nodes.append(node)
        elif text != "":
            processed_nodes.append(TextNode(text,TextType.TEXT))
    return processed_nodes

def split_nodes_link(old_nodes):
    processed_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            processed_nodes.append(node)
            continue
        text = node.text
        matches = extract_markdown_links(node.text)
        for match in matches:
            split = text.split(f"[{match[0]}]({match[1]})")
            if split[0] != "":
                processed_nodes.append(TextNode(split[0], TextType.TEXT))
            processed_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            text = split[1]
        if len(matches) == 0:
            processed_nodes.append(node)
        elif text != "":
            processed_nodes.append(TextNode(text,TextType.TEXT))
    return processed_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        if block == "\n" or block == "":
            continue
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    if not block:
        return None
    if len(re.findall(r"^(#{1,6})\s+.+$",block)) > 0:
        return BlockType.HEADING
    if len(re.findall(r"^```.+```$",block, re.DOTALL)) > 0:
        return BlockType.CODE
    if len(re.findall(r"^>\s?.+$",block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.QUOTE
    if len(re.findall(r"^\s*[-+*]\s+.+$",block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.UNORDERED_LIST
    if len(re.findall(r"^\s*\d+[.)]\s+.+$",block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
