import os
import shutil
from blocknodes import markdown_to_html_node, extract_title

def copy_files():
    source_path = os.path.normpath(os.path.join("src", "../static"))
    dest_path = os.path.normpath(os.path.join("src", "../docs"))
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)  
    def copy_item_recursive(src, dst):
        if os.path.isfile(src):
            shutil.copy(src, dst)
        elif os.path.isdir(src):
            if not os.path.exists(dst):
                os.mkdir(dst)
            for item in os.listdir(src):
                src_item = os.path.join(src, item)
                dst_item = os.path.join(dst, item)
                copy_item_recursive(src_item, dst_item)
    if os.path.exists(source_path):
        copy_item_recursive(source_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")
    with open(from_path, "r") as f1: md_contents =  f1.read()
    with open(template_path, "r") as f2:
        template_contents = f2.read() 
    html_node = markdown_to_html_node(md_contents)
    html_string = html_node.to_html()
    title = extract_title(md_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)
    template_contents = template_contents.replace('href="/', 'href="{basepath}')
    template_contents = template_contents.replace('src="/', 'src="{basepath}')
    if os.path.exists(dest_path):
        pass
    else:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as destination:
        destination.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    try:
        all_contents = os.listdir(dir_path_content)
    except FileNotFoundError:
        print(f"Error: Directory {dir_path_content} not found")
        return    
    for content in all_contents:
        current_path = os.path.join(dir_path_content, content)
        if os.path.isdir(current_path):
            rel_path = os.path.relpath(current_path, dir_path_content)
            new_dest_dir = os.path.join(dest_dir_path, rel_path)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(current_path, template_path, new_dest_dir, basepath)
        
        elif content.endswith(".md"):
            try:
                output_filename = os.path.splitext(content)[0] + ".html"
                output_path = os.path.join(dest_dir_path, output_filename)
                generate_page(current_path, template_path, output_path, basepath)
                print(f"Generated: {output_path}")
            except Exception as e:
                print(f"Error processing {current_path}: {str(e)}")


if __name__ == "__main__":
    copy_files()
    
