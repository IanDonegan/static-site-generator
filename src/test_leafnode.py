import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Link", props={"href":"https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Link</a>')


if __name__ == "__main__":
    unittest.main()
