from collections import defaultdict
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx
import pandas as pd

from docutils import core, nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import Directive, directives, roles, Parser

""" STATUS OF THIS FILE AS OF 3-Jul-2023

DOING
=====
* parsing all .rst field_list
* collecting all labels based on a hard-coded example of the field to filter by
* placing the labels inside the field "field_data"
* the content of the variable "field_data" for when it's being rendered.
* collecting the directive argument to use for the filter
* placing the content of the storage node instead of the directive

NOT DOING
=========
* insterting the table where the 1st column 'my_title' are links to the documents
"""

REPORT_FIELD_PAGETYPE = 'reportChild'
report_field_labels = ['it-policy']

# my very simple and initial attempt at setting up a node to store data
class StorageNode(nodes.Element):
    pass

class LabelRequestPlaceholderNode(nodes.General, nodes.Element):
    def __init__(self, requested_labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._requested_labels = requested_labels

    @property
    def requested_labels(self):
        return self._requested_labels

class PagePropertiesReport(SphinxDirective):
    has_content = True
    required_arguments = 1

    def run(self):
        report_field_labels = self.arguments
        requested_field_labels = [
            label.strip()
            for label in '\n'.join(report_field_labels).split(',')
        ]

        label_request_placeholder_node = LabelRequestPlaceholderNode(requested_field_labels)

        return [label_request_placeholder_node]
        # I want to replace this below with the content I stored in storage_node
        # paragraph_node = nodes.paragraph(text=f"All docs: {self.env.found_docs}\n")
        # return [paragraph_node]

    def __repr__(self):
        return str(self.val)

def get_docinfo_from_env(app, env):  # env-updated | event 10
    """Make a mapping of document names to field lists."""
    field_data = {}

    for document_name, field_metadata in env.metadata.items():
        page_type = field_metadata.get('my_pagetype', '')
        field_list = field_metadata.get('my_labels', [])
        if field_list:
            field_list = field_list.split(', ')

        if not field_list:
            continue

        if REPORT_FIELD_PAGETYPE != page_type:
            continue

        required_element_missing = any(
            element not in field_list
            for element in report_field_labels
        )
        if required_element_missing:
            continue

        field_data[document_name] = field_metadata

    env.field_data = field_data

    label_document_pairs = {  # {('l1', 'doc3'), ('l2', 'doc1'), ('l2', 'doc3')}
        (label.strip(), doc_name)
        # for doc_name, doc_meta in env.metadata.items()
        for doc_name, doc_meta in field_data.items()
        for label in doc_meta.get('my_labels', '').split(',')
    }
    label_to_document_mapping = defaultdict(set)   # label -> document names set| example data: {'l1': {'doc3'}, 'l2': {'doc1', 'doc3'}}
    # label_to_document_mapping['l1'].add('doc1')  # {'l1': {'doc1'}}
    # label_to_document_mapping['l2'] = 'stuff'
    for label, doc_name in label_document_pairs:
        label_to_document_mapping[label].add(doc_name)
    env.label_to_document_mapping = label_to_document_mapping

def create_rst_table(dataset):
    #
    # if report_columns is not defined or empty, then it will display all columns.
    report_columns = []
    report_columns = ['my_title','my_status','my_author','last_changed']

    # Create a Pandas DataFrame from the field data
    df = pd.DataFrame(dataset)
    # Transposing the table
    df_transposed = df.T
    # choosing which fields to keep in the table
    if "report_columns" in locals() or "report_columns" != []:
        df_transposed = df_transposed.loc[:,report_columns]
    # Write as rst list-table
    # footer_links will contain the refs to the rst links used in the table
    footer_links = f"\n"
    for label,content in df.items():
        content_name = content['my_title']
        content_link = f"`{content_name}`_"
        content_label = f"{label}.html"
        #df_transposed['my_title'] = df_transposed['my_title'].replace([content_name],[content_link])
        footer_links += f".. _{content_name}: {content_label}\n"
        #for html but it does NOT WORK
        #df_transposed['my_title'] = df_transposed['my_title'].replace([content_name],"<a href=" + content_label + ">" + content_link + "</a>")
        #df_transposed['my_title'] = f'<a href="{content_label}">{content_name}</a>'

    #df = df_transposed

    # show me the pandas dataframe during build
    print(df)
    print(df_transposed)
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
    table_header = f"""\n.. list-table:: Page Properties Report
    :widths: {width_str}
    :header-rows: 1\n\n"""
    # add the header RST list-table row
    table_header += "   * " + "     ".join(f"- {column}\n" for column in columns)
    # Create the RST list-table rows
    table_rows = ""
    for row in data:
        table_rows += "   * " + "     ".join(f"- {str(value)}\n" for value in row)
    # Combine the table header, rows and footer with the links
    rst_table = table_header + table_rows + footer_links

    return (rst_table)

def create_table_node(dataset):
    # alternative: creating a table_node from the pandas dataframe
    # Create a table node and add table rows
    #
    # if report_columns is not defined or empty, then it will display all columns.
    report_columns = []
    report_columns = ['my_title','my_status','my_author','last_changed']

    # Create a Pandas DataFrame from the field data
    df = pd.DataFrame(dataset)
    # Transposing the table
    df_transposed = df.T
    # choosing which fields to keep in the table
    if "report_columns" in locals() or "report_columns" != []:
        df_transposed = df_transposed.loc[:,report_columns]
    # Write as rst list-table
    # footer_links will contain the refs to the rst links used in the table
    footer_links = f"\n"
    for label,content in df.items():
        content_name = content['my_title']
        content_link = f"`{content_name}`_"
        content_label = f"{label}.html"
        #df_transposed['my_title'] = df_transposed['my_title'].replace([content_name],[content_link])
        footer_links += f".. _{content_name}: {content_label}\n"
        #for html but it does NOT WORK
        df_transposed['my_title'] = f'<a href="{content_label}">{content_name}</a>'

    # show me the pandas dataframe during build
    print(df_transposed)

    df = df_transposed

    table_node = nodes.table()
    tgroup_node = nodes.tgroup(cols=len(df.columns))
    table_node += tgroup_node

    # Create column specifications
    colspec_nodes = []
    for _ in range(len(df.columns)):
        colspec_node = nodes.colspec(colwidth=1)
        colspec_nodes.append(colspec_node)
    tgroup_node += colspec_nodes

    # Create table header row
    thead_node = nodes.thead()
    row_node = nodes.row()
    for col_name in df.columns:
        entry_node = nodes.entry()
        entry_node += nodes.paragraph(text=col_name)
        row_node += entry_node
    thead_node += row_node
    tgroup_node += thead_node

    # Create table body rows
    tbody_node = nodes.tbody()
    for _, row in df.iterrows():
        row_node = nodes.row()
        for _, value in row.items():
            entry_node = nodes.entry()
            entry_node += nodes.paragraph(text=str(value))
            row_node += entry_node
        tbody_node += row_node
    tgroup_node += tbody_node

    return(table_node)


def _make_data_table_for_requested_labels(requested_labels, document_to_filtered_data_mapping, label_to_document_mapping):
    #
    # issues with the HTML table
    # 1. the 1st column does not contain links
    # 2. the headers of the list are not included
    #
    output_format = 'rst'
    output_format = 'table_node'

    if output_format == 'table_node':
        return [create_table_node(document_to_filtered_data_mapping)]
    elif output_format == 'rst':
        return [create_rst_table(document_to_filtered_data_mapping)]

def replace_label_request_nodes_with_doc_refs(app, doctree, docname):  # doctree-resolved | event 14
    all_label_request_nodes = doctree.findall(LabelRequestPlaceholderNode)

    document_to_filtered_data_mapping = app.env.field_data
    label_to_document_mapping = app.env.label_to_document_mapping

    for label_request_placeholder_node in all_label_request_nodes:
        requested_labels = label_request_placeholder_node.requested_labels
        data_table_nodes = _make_data_table_for_requested_labels(
            requested_labels,
            document_to_filtered_data_mapping,
            label_to_document_mapping,
        )
        label_request_placeholder_node.replace_self(data_table_nodes)

def event_04_env_before_read_docs(app, env, docnames):
    # docname: {docnames} + Event env_before_read_docs
    pass

def event_06_source_read(app, docname, source):
    # docname: {docname} + Event source_read
    pass

def event_08_doctree_read(app, doctree):        # this reads the doctree for every file being processed by #06
    # doctree: {doctree} + Event doctree_read
    pass

def event_10_env_updated(app, env):
    # env.found_docs: {env.found_docs} + Event env_updated
    pass

def event_12_env_check_consistency(app, env):
    # env.found_docs: {env.found_docs} + Event env_check_consistency
    # the field data obtained from env.storage_node: {env.storage_node.field_data}
    pass

def event_14_doctree_resolved(app, doctree, docname):
    # docname: {docname} + Event source_read
    pass

def setup(app: Sphinx):
    # connecting functions to the different core events for testing/learning purposes
    # app.connect("env-before-read-docs", event_04_env_before_read_docs)             # event 04
    # app.connect("source-read", event_06_source_read)             # event 06
    # app.connect("doctree-read", event_08_doctree_read)             # event 08
    # app.connect("env-updated", event_10_env_updated)             # event 10
    # app.connect("env-check-consistency", event_12_env_check_consistency)             # event 12
    app.connect("doctree-resolved", event_14_doctree_resolved)             # event 14

    # ref from Sviatoslav
    #
    ## app.add_node(LabelRequestNode)
    ## app.add_directive('request-labels', LabelRequestDirective)
    ## app.connect('env-updated', build_label_to_document_mapping)
    ## app.connect('doctree-resolved', replace_label_request_nodes_with_doc_refs)
    #

    # the directive
    app.add_directive('page_properties_report', PagePropertiesReport)

    # when to parse the documents
        # doctree-read will process 1 doctree at a time
        # env-updated will get me the whole env with

    app.connect('doctree-resolved', replace_label_request_nodes_with_doc_refs) # all doctrees in it
    # i've decided on env-updated
    app.connect('env-updated', get_docinfo_from_env)

    # Disable caching
    app.config['env_cache'] = False
    app.config['doctree_cache'] = False
    app.config['env_purge'] = True

    return {
        'version': '1.0',
        'parallel_read_safe': False,
        'parallel_write_safe': False,
        }
