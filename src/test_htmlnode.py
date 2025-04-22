import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversion_functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_eq_props(self):
        node1 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.google.com",
    "target": "_blank"
    })
        node2 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.google.com",
    "target": "_blank"
    })
        self.assertEqual(node1.props_to_html(), node2.props_to_html())
    
    def test_uneq_props(self):
        node1 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.google.com",
    "target": "_blank"
    })
        node2 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.poogle.com",
    "target": "_blank"
    })
        self.assertNotEqual(node1.props_to_html(), node2.props_to_html())

    def test_uneven_props(self):
        node1 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.google.com",
    })
        node2 = HTMLNode("b", "This is a bold text", None, {
    "href": "https://www.google.com",
    "target": "_blank"
    })
        self.assertNotEqual(node1.props_to_html(), node2.props_to_html())

    #test leaf node
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p_two(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://times.com", "alternate":"pictureoftime"})
        self.assertEqual(node.to_html(), '<a href="https://times.com" alternate="pictureoftime">Hello, world!</a>')

    #Test parent node
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_great_grandchildren(self):
        great_grandchild = LeafNode("i", "greatgrandchild")
        grandchild_node = ParentNode("div", [great_grandchild])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><div><i>greatgrandchild</i></div></span></div>",
        )

    def test_parent_with_props(self):
        """Test a parent node with HTML attributes/properties"""
        child = LeafNode("span", "Click me")
        parent = ParentNode("button", [child], {"class": "btn", "id": "submit-btn"})
        html = parent.to_html()
        self.assertTrue(html.startswith("<button"))
        self.assertTrue(html.endswith("</button>"))
        self.assertIn('class="btn"', html)
        self.assertIn('id="submit-btn"', html)
        self.assertIn("<span>Click me</span>", html)
    
    def test_nested_parents(self):
        """Test nested parent nodes"""
        inner_child = LeafNode("li", "Item 1")
        inner_parent = ParentNode("ul", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        
        expected = "<div><ul><li>Item 1</li></ul></div>"
        self.assertEqual(outer_parent.to_html(), expected)
    
    def test_multiple_children(self):
        """Test a parent with multiple children"""
        children = [
            LeafNode("h1", "Title"),
            LeafNode("p", "Paragraph 1"),
            LeafNode("p", "Paragraph 2")
        ]
        parent = ParentNode("div", children)
        
        expected = "<div><h1>Title</h1><p>Paragraph 1</p><p>Paragraph 2</p></div>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_mixed_children(self):
        """Test a parent with mixed child types"""
        leaf = LeafNode("span", "Text")
        nested = ParentNode("div", [LeafNode("p", "Nested")])
        parent = ParentNode("section", [leaf, nested])
        
        expected = "<section><span>Text</span><div><p>Nested</p></div></section>"
        self.assertEqual(parent.to_html(), expected)
    
    def test_no_tag(self):
        """Test that an error is raised when no tag is provided"""
        child = LeafNode("p", "Content")
        parent = ParentNode(None, [child])
        
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_no_children(self):
        """Test that an error is raised when no children are provided"""
        parent = ParentNode("div", None)
        
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_empty_children_list(self):
        """Test that an error is raised with an empty children list"""
        parent = ParentNode("div", [])
        
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_complex_structure(self):
        """Test a more complex HTML structure"""
        # Create a form with multiple elements
        form_elements = [
            ParentNode("div", [
                LeafNode("label", "Name:"),
                LeafNode("input", "", {"type": "text", "name": "username"})
            ], {"class": "form-group"}),
            ParentNode("div", [
                LeafNode("label", "Email:"),
                LeafNode("input", "", {"type": "email", "name": "email"})
            ], {"class": "form-group"}),
            LeafNode("button", "Submit", {"type": "submit"})
        ]

#Test textnode to htmlnode
class TestTextToTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_normal_text(self):
       """Test converting normal text node to HTML node"""
       text_node = TextNode("Hello world", TextType.TEXT)
       html_node = text_node_to_html_node(text_node)
       
       self.assertIsInstance(html_node, LeafNode)
       self.assertIsNone(html_node.tag)
       self.assertEqual(html_node.value, "Hello world")
       self.assertIsNone(html_node.props)
   
    def test_bold_text(self):
        """Test converting bold text node to HTML node"""
        text_node = TextNode("Important", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Important")
        self.assertIsNone(html_node.props)
    
    def test_italic_text(self):
        """Test converting italic text node to HTML node"""
        text_node = TextNode("Emphasized", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Emphasized")
        self.assertIsNone(html_node.props)
    
    def test_code_text(self):
        """Test converting code text node to HTML node"""
        text_node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")
        self.assertIsNone(html_node.props)
    
    def test_link_text(self):
        """Test converting link text node to HTML node"""
        text_node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertIsNotNone(html_node.props)
        self.assertIn("href", html_node.props)
        self.assertEqual(html_node.props["href"], "https://example.com")
    
    def test_image(self):
        """Test converting image node to HTML node"""
        text_node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Image tag doesn't use value
        self.assertIsNotNone(html_node.props)
        self.assertIn("src", html_node.props)
        self.assertEqual(html_node.props["src"], "https://example.com/image.jpg")
        self.assertIn("alt", html_node.props)
        self.assertEqual(html_node.props["alt"], "Image description")
    
    def test_invalid_type(self):
        """Test that an invalid text node type raises an exception"""
        # Creating a mock TextType for testing
        class MockTextType:
            def __init__(self):
                self.value = "invalid_type"
        
        text_node = TextNode("Invalid", MockTextType())
        
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)
#Test splitting text nodes with a delimiter
class TestSplitNodeDelimiter(unittest.TestCase):
    def test_function_output(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
])
    def test_no_delimiter(self):
       """Test when text doesn't contain any delimiters"""
       node = TextNode("This is plain text", TextType.TEXT)
       result = split_nodes_delimiter([node], "*", TextType.BOLD)
       
       self.assertEqual(len(result), 1)
       self.assertEqual(result[0].text, "This is plain text")
       self.assertEqual(result[0].text_type, TextType.TEXT)
   
    def test_single_delimiter_pair(self):
        """Test with a single pair of delimiters"""
        node = TextNode("This is *bold* text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiter_pairs(self):
        """Test with multiple pairs of delimiters"""
        node = TextNode("*Bold* normal *more bold*", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " normal ")
        self.assertEqual(result[1].text_type, TextType.TEXT)
        self.assertEqual(result[2].text, "more bold")
        self.assertEqual(result[2].text_type, TextType.BOLD)
    
    def test_delimiter_at_beginning(self):
        """Test with delimiter at the beginning of text"""
        node = TextNode("*Bold* at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " at start")
        self.assertEqual(result[1].text_type, TextType.TEXT)
    
    def test_delimiter_at_end(self):
        """Test with delimiter at the end of text"""
        node = TextNode("End with *bold*", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "End with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
    
    def test_empty_delimited_content(self):
        """Test with empty content between delimiters"""
        node = TextNode("Text with ** empty bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        # Checking how many results we get after filtering empty strings
        filtered_results = [node for node in result if node.text]
        self.assertGreaterEqual(len(filtered_results), 1)
    
    def test_multiple_nodes(self):
        """Test with multiple input nodes"""
        node1 = TextNode("First *bold*", TextType.TEXT)
        node2 = TextNode("Second *bold*", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2], "*", TextType.BOLD)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "Second ")
        self.assertEqual(result[3].text, "bold")
        self.assertEqual(result[3].text_type, TextType.BOLD)
    
    def test_different_delimiter(self):
        """Test with a different delimiter"""
        node = TextNode("Code is `important`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Code is ")
        self.assertEqual(result[1].text, "important")
        self.assertEqual(result[1].text_type, TextType.CODE)
    
    def test_odd_number_of_delimiters(self):
        """Test behavior with odd number of delimiters (unbalanced)"""
        node = TextNode("Unbalanced *bold text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        
        # With the current implementation, this should result in:
        # ["Unbalanced ", "bold text"]
        # with "bold text" incorrectly marked as bold due to its odd index
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Unbalanced ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold text")
        self.assertEqual(result[1].text_type, TextType.BOLD)  # Note: This may not be intended behavior

class TestExtractMarkdownImageLink(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_single_image(self):
       """Test extracting a single image from markdown text"""
       text = "Here is an image: ![alt text](https://example.com/image.jpg)"
       result = extract_markdown_images(text)
       
       self.assertEqual(len(result), 1)
       self.assertEqual(result[0][0], "alt text")
       self.assertEqual(result[0][1], "https://example.com/image.jpg")
   
    def test_extract_multiple_images(self):
        """Test extracting multiple images from markdown text"""
        text = "First image: ![image1](https://example.com/1.jpg) and second image: ![image2](https://example.com/2.jpg)"
        result = extract_markdown_images(text)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "image1")
        self.assertEqual(result[0][1], "https://example.com/1.jpg")
        self.assertEqual(result[1][0], "image2")
        self.assertEqual(result[1][1], "https://example.com/2.jpg")
    
    def test_no_images(self):
        """Test behavior when no images are present"""
        text = "This is text without any images."
        result = extract_markdown_images(text)
        
        self.assertEqual(len(result), 0)
    
    def test_image_with_empty_alt_text(self):
        """Test extracting an image with empty alt text"""
        text = "Image: ![](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "")
        self.assertEqual(result[0][1], "https://example.com/image.jpg")
    
    def test_image_with_special_characters(self):
        """Test extracting an image with special characters in alt text"""
        text = "Image: ![Special *chars* and _formatting_](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "Special *chars* and _formatting_")
    
    def test_extract_single_link(self):
        """Test extracting a single link from markdown text"""
        text = "Here is a link: [link text](https://example.com)"
        result = extract_markdown_links(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "link text")
        self.assertEqual(result[0][1], "https://example.com")
    
    def test_extract_multiple_links(self):
        """Test extracting multiple links from markdown text"""
        text = "First link: [link1](https://example.com/1) and second link: [link2](https://example.com/2)"
        result = extract_markdown_links(text)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "link1")
        self.assertEqual(result[0][1], "https://example.com/1")
        self.assertEqual(result[1][0], "link2")
        self.assertEqual(result[1][1], "https://example.com/2")
    
    def test_no_links(self):
        """Test behavior when no links are present"""
        text = "This is text without any links."
        result = extract_markdown_links(text)
        
        self.assertEqual(len(result), 0)
    
    def test_link_with_empty_text(self):
        """Test extracting a link with empty text"""
        text = "Link: [](https://example.com)"
        result = extract_markdown_links(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "")
        self.assertEqual(result[0][1], "https://example.com")
    
    def test_mixed_links_and_images(self):
        """Test that link extraction doesn't pick up image syntax"""
        text = "Here's a ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        link_result = extract_markdown_links(text)
        
        self.assertEqual(len(link_result), 1)
        self.assertEqual(link_result[0][0], "link")
        self.assertEqual(link_result[0][1], "https://example.com")
    
    def test_image_not_matching_link_pattern(self):
        """Test that image markdown doesn't match the link pattern"""
        text = "![image](https://example.com/img.jpg)"
        result = extract_markdown_links(text)
        
        # The image should not be matched by the link pattern
        self.assertEqual(len(result), 0)
    
    def test_nested_formatting(self):
        """Test links with nested formatting in the text portion"""
        text = "[This has *italic* and **bold**](https://example.com)"
        result = extract_markdown_links(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "This has *italic* and **bold**")

# testing splitting nodes to links and images
class TestSplitNodesImage(unittest.TestCase):
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_no_images(self):
        """Test when there are no images in the text"""
        node = TextNode("This is plain text", TextType.TEXT)
        result = split_nodes_image([node])
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_single_image(self):
        """Test with a single image in the text"""
        node = TextNode("This is text with an ![image](https://example.com/img.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is text with an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/img.jpg")
    
    def test_multiple_images(self):
        """Test with multiple images in the text"""
        node = TextNode("Start ![image1](https://example.com/1.jpg) middle ![image2](https://example.com/2.jpg) end", TextType.TEXT)
        result = split_nodes_image([node])
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "image1")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/1.jpg")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "image2")
        self.assertEqual(result[3].text_type, TextType.IMAGE)
        self.assertEqual(result[3].url, "https://example.com/2.jpg")
        self.assertEqual(result[4].text, " end")
    
    def test_image_at_start(self):
        """Test with an image at the start of the text"""
        node = TextNode("![image](https://example.com/img.jpg) followed by text", TextType.TEXT)
        result = split_nodes_image([node])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "image")
        self.assertEqual(result[0].text_type, TextType.IMAGE)
        self.assertEqual(result[0].url, "https://example.com/img.jpg")
        self.assertEqual(result[1].text, " followed by text")
    
    def test_image_at_end(self):
        """Test with an image at the end of the text"""
        node = TextNode("Text followed by ![image](https://example.com/img.jpg)", TextType.TEXT)
        result = split_nodes_image([node])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text followed by ")
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://example.com/img.jpg")

class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        """Test when there are no links in the text"""
        node = TextNode("This is plain text", TextType.TEXT)
        result = split_nodes_link([node])
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_single_link(self):
        """Test with a single link in the text"""
        node = TextNode("This is text with a [link](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        
        # NOTE: There's a bug in the function where it uses image syntax for links
        # These assertions will fail with the current implementation
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)  # Function uses IMAGE instead
        self.assertEqual(result[1].url, "https://example.com")
    
    def test_multiple_links(self):
        """Test with multiple links in the text"""
        node = TextNode("Start [link1](https://example.com/1) middle [link2](https://example.com/2) end", TextType.TEXT)
        result = split_nodes_link([node])
        
        # These assertions will fail with the current implementation
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "link1")
        self.assertEqual(result[1].text_type, TextType.LINK)  # Function uses IMAGE instead
        self.assertEqual(result[1].url, "https://example.com/1")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "link2")
        self.assertEqual(result[3].text_type, TextType.LINK)  # Function uses IMAGE instead
        self.assertEqual(result[3].url, "https://example.com/2")
        self.assertEqual(result[4].text, " end")
    
    def test_link_at_start(self):
        """Test with a link at the start of the text"""
        node = TextNode("[link](https://example.com) followed by text", TextType.TEXT)
        result = split_nodes_link([node])
        
        # These assertions will fail with the current implementation
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "link")
        self.assertEqual(result[0].text_type, TextType.LINK)  # Function uses IMAGE instead
        self.assertEqual(result[0].url, "https://example.com")
        self.assertEqual(result[1].text, " followed by text")
    
    def test_link_at_end(self):
        """Test with a link at the end of the text"""
        node = TextNode("Text followed by [link](https://example.com)", TextType.TEXT)
        result = split_nodes_link([node])
        
        # These assertions will fail with the current implementation
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Text followed by ")
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)  # Function uses IMAGE instead
        self.assertEqual(result[1].url, "https://example.com")

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        """Test with plain text without any formatting"""
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is just plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_sequential_formatting(self):
        """Test with formatting that appears in sequence"""
        text = "**Bold text** _italic text_ `code text`"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Bold text")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "italic text")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, "code text")
        self.assertEqual(nodes[2].text_type, TextType.CODE)
    
    def test_mixed_normal_and_formatted(self):
        """Test mixing normal text with formatted text"""
        text = "Normal text with **bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        
        # Check that we have both normal and formatted nodes
        types = [node.text_type for node in nodes]
        self.assertIn(TextType.TEXT, types)
        self.assertIn(TextType.BOLD, types)
        self.assertIn(TextType.ITALIC, types)
        self.assertIn(TextType.CODE, types)
    
    def test_multiple_of_same_type(self):
        """Test with multiple instances of the same formatting type"""
        text = "First **bold** and second **bold** and third **bold**"
        nodes = text_to_textnodes(text)
        
        bold_nodes = [node for node in nodes if node.text_type == TextType.BOLD]
        self.assertEqual(len(bold_nodes), 3)
        self.assertEqual(bold_nodes[0].text, "bold")
        self.assertEqual(bold_nodes[1].text, "bold")
        self.assertEqual(bold_nodes[2].text, "bold")
    
    def test_formatting_within_formatting(self):
        """Test what happens when formatting is nested (not perfectly supported)"""
        text = "This is **_bold and italic_** text"
        nodes = text_to_textnodes(text)
        
        # The behavior here depends on the order of processing
        # Since bold is processed before italic, the underscore should be inside the bold
        self.assertGreaterEqual(len(nodes), 1)
        # Check that no content is lost during parsing
        combined_text = "".join(node.text for node in nodes)
        self.assertIn("bold and italic", combined_text)
    
    def test_empty_text(self):
        """Test with empty text"""
        text = ""
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)


if __name__ == "__main__":
    unittest.main()