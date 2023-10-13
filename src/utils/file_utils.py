# file_utils.py
import os
import streamlit as st

ALLOWED_EXTENSIONS = set(['csv', 'py', 'js', 'txt'])

EXTENSION_ICONS = {
    'csv': '📊',
    'py': '🐍',
    'js': '📜',
    'txt': '📝',
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def display_directory_tree(path, indent=0):
    tree = {}
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree[item] = display_directory_tree(item_path, indent + 1)
        else:
            tree[item] = None
    return tree


def render_directory_tree(tree, indent=2):
    for item, content in tree.items():
        extension = item.split('.')[-1].lower() if '.' in item else None
        icon = EXTENSION_ICONS.get(extension, '📄') if extension else '📁'
        if content is None:
            st.text("\u200B" + " " * indent + f"{icon} {item}")
        else:
            st.text("\u200B" + " " * indent + f"{icon} {item}")
            render_directory_tree(content, indent + 2)