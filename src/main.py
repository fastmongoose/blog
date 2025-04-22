# print("hello world")
from textnode import TextNode, TextType
from copy_contents import copy_files, generate_pages_recursive
import os

def main():
    copy_files()
    source = os.path.normpath(os.path.join("src", "../content/"))
    destination = os.path.normpath(os.path.join("src", "../public/"))
    template = os.path.normpath(os.path.join("src", "../template.html"))
    generate_pages_recursive(source, template, destination)

if __name__ == "__main__":
    main()