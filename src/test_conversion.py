import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from conversion import *

class TestTextNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, None)
        self.assertEqual(leaf.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "i")
        self.assertEqual(leaf.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "code")
        self.assertEqual(leaf.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.value, "This is a link node")
        self.assertEqual(leaf.props["href"], "https://example.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com")
        leaf = text_node_to_html_node(node)
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.value, "")
        self.assertEqual(leaf.props["alt"], "This is an image node")
        self.assertEqual(leaf.props["src"], "https://example.com")

    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_node_delimiter_code_2(self):
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_node_delimiter_code_3(self):
        node = TextNode("`code block` plus text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code block", TextType.CODE),
            TextNode(" plus text", TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_node_delimiter_bold(self):
        node = TextNode("**bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_node_delimiter_italic(self):
        node = TextNode("_italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(expected, new_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_empty_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_blank(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual( blocks, [],)

    def test_block_to_block_type_paragraph(self):
        md = """
This is a paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))

    def test_block_to_block_type_heading(self):
        md = """
## This is a heading.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.HEADING, block_to_block_type(blocks[0]))

    def test_block_to_block_type_code(self):
        md = """
```
This is code.
```
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.CODE, block_to_block_type(blocks[0]))

    def test_block_to_block_type_code_unclosed(self):
        md = """
```
This is code.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))

    def test_block_to_block_type_quote(self):
        md = """
> This is a quote.
> This is another quote.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.QUOTE, block_to_block_type(blocks[0]))

    def test_block_to_block_type_quote_incomplete(self):
        md = """
> This is a quote.
This is non-quote
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))

    def test_block_to_block_type_ordered(self):
        md = """
1. This is line one.
2. This is line two.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(blocks[0]))

    def test_block_to_block_type_ordered_incomplete(self):
        md = """
1. This is line one.
This is line two.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))

    def test_block_to_block_type_unordered(self):
        md = """
- This is line one.
- This is line two.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(blocks[0]))

    def test_block_to_block_type_unordered_incomplete(self):
        md = """
- This is line one.
This is line two.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(blocks[0]))

    def test_block_to_block_type_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        with self.assertRaises(IndexError):
            block_to_block_type(blocks[0])

    def test_block_to_block_type_none(self):
        md = None
        with self.assertRaises(AttributeError):
            blocks = markdown_to_blocks(md)

if __name__ == "__main__":
    unittest.main()
