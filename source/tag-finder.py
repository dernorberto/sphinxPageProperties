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

children_with_set_tags = []     # list holding the children docs
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
field_data = {}

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
    # Add the current file to the dict
    field_data.update({rst_file_path: {}})
    # Process field lists
    for field_list_node in field_list_nodes:
        field_name = field_list_node.children[0].astext()
        field_value = field_list_node.children[1].astext()
        #print(f"{field_name} = {field_value}")         # troubleshooting help

        # I need a data structure like this:
        # | file | field: Author | field: Title | field: tags | last_changed | pagetype |
        # so the list would be
        # [ file01: {myAuthor : author, myTitle: title, myTags: tags} ,
        #   file02: {myAuthor : author, myTitle: title, myTags: tags} ,
        # ]

        field_data[rst_file_path].update({field_name:field_value})

# Create a Pandas DataFrame from the field data
df = pd.DataFrame(field_data)

# Transposing the table
df_transposed = df.T

## Write table to RST file
# chosing which fields to keep in the table
df_transposed = df_transposed.loc[:,['my_title','my_pagetype','my_author', 'my_labels', 'last_changed']]

# replace myTitle with a link to the corresponding HTML file
# Format: `Link text <https://domain.invalid/>`_
# Example: `Child Page 03 <1-child-03.html>`_
# current: Child Page 03
# target: take the header for the column from 'df' and replace the .rst with .html
## something along these lines:
#df_transposed['myTitle'] = df_transposed['myTitle'].replace(['Child Page 03'],["`Child Page 03`_"])

footer_links = f"\n"
for label,content in df.items():
    content_name = content['my_title']
    content_link = f"`{content_name}`_"
    content_label = label.replace(".rst",".html")
    df_transposed['my_title'] = df_transposed['my_title'].replace([content_name],[content_link])
    footer_links += f".. _{content_name}: {content_label}\n"


# Get the column names and data from the DataFrame
columns = df_transposed.columns.tolist()
data = df_transposed.values.tolist()

# Calculate the maximum width of each column
column_widths = [max(len(str(value)) for value in column) for column in zip(*data)]
header_widths = [len(str(element)) for element in columns]

# pick the widest between the values or the headers
counter = 0
for n in column_widths:
    if header_widths[counter] > n:
        column_widths[counter] = header_widths[counter]
    counter = counter + 1

# Create the RST table header
table_header = f"+{'+'.join(['-' * (width + 2) for width in column_widths])}+\n"
table_header += "| " + " | ".join(f"{column.center(width)}" for column, width in zip(columns, column_widths)) + " |\n"
table_header += f"+{'+'.join(['=' * (width + 2) for width in column_widths])}+\n"


# Create the RST table rows
table_rows = ""
for row in data:
    table_rows += "| " + " | ".join(f"{str(value).ljust(width)}" for value, width in zip(row, column_widths)) + " |\n"
    table_rows += f"+{'+'.join(['-' * (width + 2) for width in column_widths])}+\n"

# Combine the table header and rows
rst_table = table_header + table_rows + footer_links

print(rst_table)

# Create the .rst file with the table
with open("page_properties_table.rst", 'w', encoding='utf-8') as file:
    file.write("""Page Properties Table
===========================

""")
    file.write(rst_table)
    file.close()