from sphinx.application import Sphinx
import pandas as pd
import os
import argparse

"""
Rewritten version of the field-finder.py that does not need docutils and has much less errors.

"""

parser = argparse.ArgumentParser()
parser.add_argument('labels',
                    nargs='+',
                    help="1 or more labels to use as a filter")
#parser.add_argument('--columns',
#                    type=list,
#                    nargs='+',
#                    help='Columns to display',
#                    default=['my_title','my_status','last_changed'],
#                    required=False)
args = parser.parse_args()

current_dir = os.getcwd()
source_dir = current_dir
build_dir = os.path.join(current_dir,'_build')
doctree_dir = os.path.join(current_dir,'_doctrees')
report_field_pagetype = 'reportChild'
report_field_labels = args.labels
#report_field_labels = 'it-policy'
report_columns = ['my_title','my_status','last_changed']
#report_columns = args.columns

sphinx_overrides = {
        'exclude_patterns': ['_tags/**',
                             'archive/**',
                             'templates/**',
                             'page_properties_table.rst',
                             ]
    }

sphinx_app = Sphinx(source_dir,source_dir,build_dir,doctree_dir,'html',freshenv=True,verbosity=0,confoverrides=sphinx_overrides)
sphinx_app.build(False)     # build the app to parse the files and access the metadata

docs_all = list(sphinx_app.env.found_docs)      # convert the set into a list

docs_for_pageproperties = []     # list holding the children docs
rst_content = ""

# List for Field List dicts
field_data = {}

# Fill dict with metadata from docs with metadata, will skip empty metadata
for n in docs_all:
    field_metadata = sphinx_app.env.metadata[n]
    if field_metadata != {}:
        if 'my_pagetype' in field_metadata:
            if report_field_pagetype in field_metadata['my_pagetype']:
                if 'my_labels' in field_metadata:
                    field_list = field_metadata['my_labels'].split(', ')
                    # check if all elements of report_field_labels are in field_list
                    if all(element in field_list for element in report_field_labels):
                        # if True, then add to field_data
                        field_data.update({n:{}})
                        field_data[n].update(sphinx_app.env.metadata[n])

print(f"There are {len(field_data)} pages that meet the criteria")

# Create a Pandas DataFrame from the field data
df = pd.DataFrame(field_data)

# Transposing the table
df_transposed = df.T

## Write table to RST file
# chosing which fields to keep in the table
df_transposed = df_transposed.loc[:,report_columns]

print(f"\nThe dataframe:")
print(f"\n{df_transposed}\n")

footer_links = f"\n"
for label,content in df.items():
    content_name = content['my_title']
    content_link = f"`{content_name}`_"
    content_label = f"{label}.html"
    #content_label = label.replace(".rst",".html")
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

# Create the RST list-table header
width_str = ' '.join(str(e) for e in column_widths)
table_header = f""".. list-table:: Page Properties Report
   :widths: {width_str}
   :header-rows: 1

"""
# add the header RST list-table row
table_header += "   * " + "     ".join(f"- {column}\n" for column in columns)

# Create the RST list-table rows
table_rows = ""
for row in data:
    table_rows += "   * " + "     ".join(f"- {str(value)}\n" for value in row)

# Combine the table header and rows
rst_table = table_header + table_rows + footer_links

print(f"\nThe table we are creating:\n")
print(rst_table)

# Create the .rst file with the table
with open("page_properties_table.rst", 'w', encoding='utf-8') as file:
    file.write("""Page Properties Table
===========================

""")
    file.write(rst_table)
    file.close()