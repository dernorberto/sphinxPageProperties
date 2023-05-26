from docutils.core import publish_doctree
from docutils import nodes
from sphinx.application import Sphinx
import pandas as pd
import os

current_dir = os.getcwd()
source_dir = current_dir
build_dir = os.path.join(current_dir,'_build')
doctree_dir = os.path.join(current_dir,'_doctrees')
my_directive = 'tags'
my_report_tag = 'typeReportChild'

sphinx_app = Sphinx(source_dir,source_dir,build_dir,doctree_dir,'html',verbosity=0)

my_env = sphinx_app.env
all_files = my_env.found_docs

tagstart = ".. tags::"
tagend = ""
children_with_set_tags = []
rst_content = ""
for file_path in all_files:
    with open(f"{file_path}.rst", 'r', encoding='utf-8') as file:
        rst_content = file.read()
    if f".. tags::" in rst_content:
        for line in rst_content.split("\n"):
            if tagstart in line:
                tagline = line.replace(tagstart, "").rstrip(tagend)
                my_tags = tagline.split(",")
                my_tags = [tag.strip() for tag in my_tags]
                print(f"File: {file_path}.rst, directive: '{my_directive}', values {my_tags}")
                if my_report_tag in my_tags:
                    children_with_set_tags.append(f"{file_path}.rst")

# List to store field data
field_data = []

for rst_file_path in children_with_set_tags:
    rst_content = ""
    with open(rst_file_path, 'r') as rst_file:
        ## rst_content = rst_file.read()
        lines = rst_file.readlines()
        for line in lines:
            if '.. tags::' in line:
                pass
            else:
                rst_content += line

    # Parse the RST content
    doctree = publish_doctree(rst_content)

    # Find all field list nodes
    field_list_nodes = doctree.traverse(nodes.field)

    # Process field lists
    for field_list_node in field_list_nodes:
        field_name = field_list_node.children[0].astext()
        field_value = field_list_node.children[1].astext()

          # Add field data to the list
        field_data.append({'File': rst_file_path, 'Field': field_name, 'Value': field_value})

# Create a Pandas DataFrame from the field data
df = pd.DataFrame(field_data)