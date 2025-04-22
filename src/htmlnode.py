class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        all_props = []
        if not self.props:
            return ""
        for key, value in self.props.items():
            all_props.append(f' {key}="{value}"')
        return "".join(all_props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have a tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        def traverse_nodes(children):
            html_text = f""
            for child in children:
                if isinstance(child, LeafNode):
                    html_text += child.to_html()
                elif isinstance(child, ParentNode):
                    html_text += f"<{child.tag}{child.props_to_html()}>" + traverse_nodes(child.children) + f"</{child.tag}{child.props_to_html()}>"
            return html_text
        text = f"<{self.tag}{self.props_to_html()}>" + traverse_nodes(self.children) + f"</{self.tag}>"
        return text


