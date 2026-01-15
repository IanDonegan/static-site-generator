import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different text node", TextType.LINK)
        node4 = TextNode("This is a link Node", TextType.ITALIC, "https://localhost")
        node5 = TextNode("This is a link Node", TextType.ITALIC, "https://localhost")
        self.assertEqual(node, node2)
        self.assertEqual(node4, node5)
        self.assertNotEqual(node, node3)


if __name__ == "__main__":
    unittest.main()
