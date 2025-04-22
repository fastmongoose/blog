# print("hello world")
from textnode import TextNode, TextType
from copy_contents import copy_files, generate_pages_recursive
import os
import sys

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_files()
    source = os.path.normpath(os.path.join("src", "../content/"))
    destination = os.path.normpath(os.path.join("src", "../docs/"))
    template = os.path.normpath(os.path.join("src", "../template.html"))
    generate_pages_recursive(source, template, destination, basepath)

if __name__ == "__main__":
    main()