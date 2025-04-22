from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
import re

def text_node_to_html_node(text_node):
    if text_node.text_type.value == "text":
        return LeafNode(tag=None,value = text_node.text)
    elif text_node.text_type.value == "bold":
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type.value == "italic":
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type.value == "code":
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type.value == "link":
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type.value == "image":
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text} )
    else:
        raise Exception("Not a valid text node")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    parsed_node_list = []
    for node in old_nodes:
        node_split = node.text.split(delimiter)
        if len(node_split) > 1:
            for i in range(len(node_split)):
                if node_split[i] == "":
                    continue
                if i%2 == 0:
                    parsed_node_list.append(TextNode(node_split[i], TextType.TEXT))
                else:
                    parsed_node_list.append(TextNode(node_split[i], text_type))
        else:
            parsed_node_list.append(node)
    return parsed_node_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    return_list = []
    for node in old_nodes:
        node_extracted = []
        all_text = node.text
        extracted_images = extract_markdown_images(node.text)
        split_text = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", all_text)
        split_text = list(filter(None, split_text))
        if not split_text:
            return [node]
        for item in split_text:
            if not item or item.isspace():
                continue
            if not extract_markdown_images(item):
                return_list.append(TextNode(item, TextType.TEXT))
            else:
                return_list.append(TextNode(extract_markdown_images(item)[0][0], TextType.IMAGE, extract_markdown_images(item)[0][1]))
    return return_list

def split_nodes_link(old_nodes):
    return_list = []
    for node in old_nodes:
        node_extracted = []
        all_text = node.text
        extracted_images = extract_markdown_links(node.text)
        split_text = re.split(r"((?<!!)\[[^\[\]]*\]\([^\(\)]*\))", all_text)
        split_text = list(filter(None, split_text))
        if not split_text:
            return [node]
        for item in split_text:
            if not item or item.isspace():
                continue
            if not extract_markdown_links(item):
                return_list.append(TextNode(item, TextType.TEXT))
            else:
                return_list.append(TextNode(extract_markdown_links(item)[0][0], TextType.LINK, extract_markdown_links(item)[0][1]))
    return return_list

def text_to_textnodes(text):
    # start with whole text, process, images, links, bold, italic, code
    return_nodes = []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    for node in nodes:
        if not node.text.isspace():
            return_nodes.append(node)
    return return_nodes

def markdown_to_blocks(markdown):
    parsed_md = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block:
            parsed_md.append(block.strip())
    return parsed_md
