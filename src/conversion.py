import re

from leafnode import LeafNode
from htmlnode import HTMLNode
from textnode import TextNode, TextType

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
    return processed_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
