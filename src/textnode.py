from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text is not other.text:
            return False
        if self.text_type is not other.text_type:
            return False
        if self.url is not other.url:
            return False
        return True

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
