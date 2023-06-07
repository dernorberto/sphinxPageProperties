from docutils.core import publish_doctree
from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("label", type=str,
                    help="The label to use as a filter")
args = parser.parse_args()

current_dir = os.getcwd()
source_dir = current_dir
build_dir = os.path.join(current_dir,'_build')
doctree_dir = os.path.join(current_dir,'_doctrees')
report_field_pagetype = 'reportChild'
report_field_label = args.label
#report_field_label = 'it-policy'

sphinx_overrides = {
        'exclude_patterns': ['_tags/**',
                             'archive/**',
                             'templates/**',
                             'page_properties_table.rst',
                             ]
    }

class SkipDirective(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        # Return an empty list to indicate that the directive should be skipped
        return []

def setup(app):
    app.add_directive('tags', SkipDirective)
    app.add_directive('toctree', SkipDirective)
    app.add_directive('autoclass', SkipDirective)
    app.add_directive('autofunction', SkipDirective)
    app.add_directive('automodule', SkipDirective)
    app.add_directive('autodoc', SkipDirective)
    app.add_directive('code-block', SkipDirective)
    app.add_directive('literalinclude', SkipDirective)
    app.add_directive('image', SkipDirective)
    app.add_directive('seealso', SkipDirective)
    app.add_directive('versionadded', SkipDirective)
    app.add_directive('versionchanged', SkipDirective)

sphinx_app = Sphinx(source_dir,source_dir,build_dir,doctree_dir,'html',freshenv=True,verbosity=0,confoverrides=sphinx_overrides)
#setup(sphinx_app)      # not running this as I'd like to not depend on this docutils limitation

env = sphinx_app.env
docs_all = sphinx_app.env.found_docs

docs_for_pageproperties = []     # list holding the children docs

rst_content = ""

def parse_file_header(arg_file_path):
    rst_content = ""
    with open(f"{arg_file_path}.rst", 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(':') == False:
                pass
            else:
                rst_content += line
    try:
        doctree = publish_doctree(rst_content, settings_overrides={'traceback': True})    
    except Exception as e:
        print("Error:", e)

    return(doctree)

# List for Field List dicts
field_data = {}

def fields_get(arg_file_path,arg_doctree):
    # Find all field list nodes
    field_nodes = arg_doctree.traverse(nodes.field)
    #field_list_nodes = arg_doctree.traverse(nodes.field_list)      # returns empty
    nodes_list = []
    nodes_names = []
    nodes_values = []
    field_data.update({arg_file_path: {}})
    for n in field_nodes:   # get all the fields
        field_name = n.children[0].astext()
        nodes_names.append(field_name)
        field_value = n.children[1].astext()
        nodes_values.append(field_value)
        nodes_list.append({field_name:field_value})         # append list with key value pair dicts
        field_data[arg_file_path].update({field_name:field_value})


    if 'my_labels' in nodes_names:           # check the correct my_pagetype
        my_index = nodes_names.index('my_labels')
        if report_field_label in nodes_values[my_index]:
            if 'my_pagetype' in nodes_names:           # check the correct my_pagetype
                my_index = nodes_names.index('my_pagetype')
                if report_field_pagetype in nodes_values[my_index]:
                    docs_for_pageproperties.append(arg_file_path)
                #else:
                    #print(f"Did not find reportChild in my_pagetype")
            #else:
                #print(f"Did not find 'my_pagetype' in field lists")
        #else:
            #print(f"Did not find 'it-policy' in my_labels")
    #else:
        #print(f"Did not find 'my_labels' in fields lists")

    if arg_file_path not in docs_for_pageproperties :
        field_data.pop(arg_file_path)
            
""" What I need
[x] get all docs
[x] check fields for those we need
[x] get a list of the docs we need
[x] get fields from those we need
"""

for my_doc in docs_all:
    my_doctree = parse_file_header(my_doc)
    fields_get(my_doc,my_doctree)

# Create a Pandas DataFrame from the field data
df = pd.DataFrame(field_data)

# Transposing the table
df_transposed = df.T

## Write table to RST file
# chosing which fields to keep in the table
df_transposed = df_transposed.loc[:,['my_title','my_status','last_changed']]

print(f"\n{df_transposed}\n")

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