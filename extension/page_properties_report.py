from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
from sphinx.application import Sphinx
import pandas as pd
import os
#from sphinx.util import logging
#import logging

from sphinx.util import logging
logger = logging.getLogger(__name__)

"""
Rewritten version of the field-finder.py that does not need docutils and has much less errors.

"""

#def run(app):
#    print(f"app.self = {app.self}")

class PagePropertiesReport(SphinxDirective):

    has_content = True
    required_arguments = 1

    def run(self):

        report_field_pagetype = 'reportChild'
        report_field_labels = self.arguments

        sphinx_overrides = {
                'exclude_patterns': ['_tags/**',
                                    'archive/**',
                                    'templates/**',
                                    'page_properties_table.rst',
                                    ]
            }

        logger.info(f"self.env.metadata: {self.env.metadata}\n")
        docs_all = self.env.found_docs
        paragraph_node = nodes.paragraph(text=f"All docs: {str(docs_all)}\n")       # OK!!!
        data = get_field_data(self,report_field_labels)

        docs_all = list(self.env.found_docs)

        return [paragraph_node]

    def process_metadata(self, app, doctree):
        logger.info(f"Running process_metadata(self, app, doctree)\n")

        docname = app.env.docname
        logger.info(f"docname: {docname}\n")
        metadata = app.env.metadata[docname]
        logger.info(f"app.env.metadata[docname]: {metadata}\n")
        # Process the metadata as needed

    def setup(self):
        print(f"Running setup(self)")
        self.app.connect("doctree-read", self.process_metadata)


def get_field_data(app,labels):
    report_field_pagetype = 'reportChild'
    report_field_labels = labels
    logger.info(f"Labels = {report_field_labels}\n")
    docs_all = list(app.env.found_docs)      # convert the set into a list

    docs_for_pageproperties = []     # list holding the children docs
    rst_content = ""

    # List for Field List dicts
    field_data = {}

    # Fill dict with metadata from docs with metadata, will skip empty metadata
    for n in docs_all:
        field_metadata = app.env.metadata[n]
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
                        else:
                            logger.info(f"report_field list: {field_list}")
                    else:
                        logger.info(f"my_labels not present in field_metadata")

    logger.info(f"There are {len(field_data)} pages that meet the criteria")
    return [field_data]

def print_metadata(app):
    for docname, document in app.env.found_docs:
        metadata = document.metadata
        logger.info(f"Metadata for document '{docname}':")
        logger.info(metadata)
        logger.info("-------------------------")



def create_table(data):
    # Create a Pandas DataFrame from the field data
    df = pd.DataFrame(data)

    # Transposing the table
    df_transposed = df.T

    ## Write table to RST file
    # chosing which fields to keep in the table
    report_columns = ['my_title','my_status','last_changed']
    df_transposed = df_transposed.loc[:,report_columns]

    logger.info(f"\nThe dataframe:")
    logger.info(f"\n{df_transposed}\n")

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

    #table_node = nodes.paragraph(text = rst_table)
    return [rst_table]



def setup(app):
    #app.connect("builder-inited", print_metadata)
#    logging.basicConfig(level=logging.DEBUG)
    app.add_directive('pagepropertiesreport', PagePropertiesReport)
    app.connect("doctree-read", get_field_data)

    return {
        'version': '1.0',
        'parallel_read_safe': False,
        'parallel_write_safe': False,
        }
