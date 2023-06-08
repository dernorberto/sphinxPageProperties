from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
from sphinx.application import Sphinx
import pandas as pd
import os
from sphinx.util import logging
logger = logging.getLogger(__name__)

report_field_pagetype = 'reportChild'
field_data = {}
report_field_labels = ""
report_columns = ['my_title','my_status','last_changed']

"""
Rewritten version of the field-finder.py that does not need docutils and has much less errors.

"""

class PagePropertiesReport(SphinxDirective):

    has_content = False
    required_arguments = 1

    def run(self):

        report_field_labels = self.arguments

        """ commenting out due to AttributeError("'function' object has no attribute 'sphinx_overrides'")
                sphinx_overrides = {
                        'exclude_patterns': ['_tags/**',
                                            'archive/**',
                                            'templates/**',
                                            'page_properties_table.rst',
                                            ]
                    }
        """
        #docs_all = list(self.env.found_docs)
#        content = {}
#        content = content.update(field_data)
#        print(f"content type = {type(content)}\n")
#        print(f"content = {field_data}")

        paragraph_node = nodes.paragraph(text=f"All docs: {self.env.found_docs}\n")
        #paragraph_node = nodes.paragraph(text=f"All docs: {str(field_data)}\n")       # OK!!!

        return [paragraph_node]

def create_table(data):
    # Create a Pandas DataFrame from the field data
    df = pd.DataFrame(data)

    # Transposing the table
    df_transposed = df.T

    ## Write table to RST file
    # chosing which fields to keep in the table

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
    return(rst_table)

def on_10_env_updated(app, env):
    logger.info(f"\nEvent: ENV-UPDATED\n")
    # env.found_docs
    # env.longtitles
    # env.metadata[docname]       --> dict?

    for m in env.metadata:
        field_metadata = env.metadata[m]    # set var to hold metadata
        if field_metadata != {}:
            if 'my_pagetype' in field_metadata:
                if report_field_pagetype in field_metadata['my_pagetype']:
                    if 'my_labels' in field_metadata:
                        field_list = field_metadata['my_labels'].split(', ')
                        # check if all elements of report_field_labels are in field_list
                        if all(element in field_list for element in report_field_labels):
                            # if True, then add to field_data
                            field_data.update({m:{}})
                            field_data[m].update(field_metadata)
                        else:
                            logger.info(f"report_field list: {field_list}")
                    else:
                        logger.info(f"my_labels not present in field_metadata")
    logger.info(f"There are {len(field_data)} pages that meet the criteria")
    return (field_data)

    #return(field_data)

def on_06_source_read(app, docname, source):
    logger.info(f"\nEvent: SOURCE-READ\n")
    for m in env.metadata:
        field_metadata = env.metadata[m]    # set var to hold metadata
        if field_metadata != {}:
            if 'my_pagetype' in field_metadata:
                if report_field_pagetype in field_metadata['my_pagetype']:
                    if 'my_labels' in field_metadata:
                        field_list = field_metadata['my_labels'].split(', ')
                        # check if all elements of report_field_labels are in field_list
                        if all(element in field_list for element in report_field_labels):
                            # if True, then add to field_data
                            field_data.update({m:{}})
                            field_data[m].update(field_metadata)
                        else:
                            logger.info(f"report_field list: {field_list}")
                    else:
                        logger.info(f"my_labels not present in field_metadata")
    logger.info(f"There are {len(field_data)} pages that meet the criteria")
    return [field_data]

def on_08_doctree_read(app, doctree):
    logger.info(f"\nEvent: DOCTREE-READ\n")
    pass



def setup(app):
    app.connect("env-updated", on_10_env_updated)
    app.add_directive('pagepropertiesreport', PagePropertiesReport)
#    app.connect("env-before-read-docs", on_04_env_before_read_docs)        # it only catches the source from previous files
#    app.connect("doctree-read", get_field_data)
#    app.connect("source-read", on_06_source_read)
#    app.connect("doctree-read", on_08_doctree_read)

    # Create an instance of PagePropertiesData
    page_properties_data = PagePropertiesData()

    # Connect the data collection handler to the doctree-read event
    app.connect("doctree-read", page_properties_data.collect_fields)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }


################

