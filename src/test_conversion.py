import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from conversion import text_node_to_html_node, split_nodes_delimiter

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

if __name__ == "__main__":
    unittest.main()
