import unittest
from conversion_functions import markdown_to_blocks
from blocknodes import BlockType, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
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
    def test_simple_two_blocks(self):
       """Test splitting markdown with two simple blocks"""
       markdown = "This is the first paragraph\n\nThis is the second paragraph"
       result = markdown_to_blocks(markdown)
       
       self.assertEqual(len(result), 2)
       self.assertEqual(result[0], "This is the first paragraph")
       self.assertEqual(result[1], "This is the second paragraph")
   
    def test_multiple_blank_lines(self):
        """Test with multiple blank lines between blocks"""
        markdown = "First block\n\n\n\nSecond block"
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "First block")
        self.assertEqual(result[1], "Second block")
    
    def test_leading_and_trailing_spaces(self):
        """Test that leading and trailing spaces are stripped"""
        markdown = "   First block   \n\n   Second block   "
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "First block")
        self.assertEqual(result[1], "Second block")
    
    def test_empty_blocks(self):
        """Test that empty blocks are not included"""
        markdown = "First block\n\n\n\nSecond block\n\n\n\n"
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "First block")
        self.assertEqual(result[1], "Second block")
    
    def test_single_block(self):
        """Test with a single block"""
        markdown = "This is just one block"
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "This is just one block")
    
    def test_empty_markdown(self):
        """Test with empty markdown"""
        markdown = ""
        result = markdown_to_blocks(markdown)
        
        self.assertEqual(len(result), 0)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_blocks(self):
        """Test different levels of heading blocks"""
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_not_heading_block(self):
        """Test that incorrectly formatted headings are not identified as headings"""
        self.assertEqual(block_to_block_type("#Incorrect Heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("##Not a heading"), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        """Test code blocks"""
        self.assertEqual(block_to_block_type("```\ncode line 1\ncode line 2\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\ndef function():\n    pass\n```"), BlockType.CODE)
    
    def test_not_code_block(self):
        """Test that incorrectly formatted code blocks are not identified as code"""
        self.assertEqual(block_to_block_type("```\ncode without closing backticks"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("not a ```code block```"), BlockType.PARAGRAPH)
    
    def test_quote_block(self):
        """Test quote blocks"""
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2\n> Line 3"), BlockType.QUOTE)
    
    def test_not_quote_block(self):
        """Test incorrectly formatted quote blocks"""
        self.assertEqual(block_to_block_type("> Line 1\nLine 2 without >"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Not a > quote"), BlockType.PARAGRAPH)
    
    def test_unordered_list_block(self):
        """Test unordered list blocks"""
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list_block(self):
        """Test incorrectly formatted unordered lists"""
        self.assertEqual(block_to_block_type("- Item 1\nItem 2 without -"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("-Not a list item"), BlockType.PARAGRAPH)
    
    def test_ordered_list_block(self):
        """Test ordered list blocks"""
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)
    
    def test_not_ordered_list_block(self):
        """Test incorrectly formatted ordered lists"""
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 3 (skipped 2)"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Item 1\nItem 2 without number"), BlockType.PARAGRAPH)
    
    def test_paragraph_block(self):
        """Test paragraph blocks"""
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("This is a paragraph\nwith multiple lines"), BlockType.PARAGRAPH)
    
    def test_mixed_content(self):
        """Test blocks with mixed content that should be paragraphs"""
        self.assertEqual(block_to_block_type("Text with # inside"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. Not a list\nBecause of this line"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- Not a list\nBecause of this line"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> Not a quote\nBecause of this line"), BlockType.PARAGRAPH)

    # Final markdown to html node testing
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()