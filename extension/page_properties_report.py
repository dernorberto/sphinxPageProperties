from collections import defaultdict
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx
import pandas as pd
from docutils import core
from docutils.core import publish_doctree, publish_parts
from docutils.parsers.rst import Directive, directives, roles, Parser

"""_summary_
        Key-Value pairs are added as field_names to documents, which can then be summarized
        in a table by calling the page_properties_report directive.

"""

REPORT_FIELD_PAGETYPE = 'reportChild'
report_field_labels = []

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
        # hacky way to split the argument if comma-separated without a space
        my_arguments = str(self.arguments[0])
        if "," in self.arguments[0]:
            globals()["report_field_labels"] = my_arguments.split(',')
        else:
            globals()["report_field_labels"] = (self.arguments)

        requested_field_labels = report_field_labels

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


def create_table_node(dataset):
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
    # create the table node
    table_node = nodes.table()      # OK
    # amount of columns in a variable
    columns_number = len(report_columns)
    # Create a tgroup node to define the table structure:
    table_group_node = nodes.tgroup(cols=columns_number)
    table_node += table_group_node
    # Create colspec nodes to define column specifications
    # syntax "nodes.colspec(colwidth=1)"
    colspec_nodes = []
    for c_width in column_widths:
        nodes.colspec(colwidth=c_width)
        colspec_nodes.append(nodes.colspec(colwidth=c_width))
    table_group_node += colspec_nodes

    # Create the thead nodes and add them to the table
    table_head_node = nodes.thead()
    table_head_node_title = nodes.thead()   # for the Page Properties title

    title_row = nodes.row()
    title_row += nodes.entry('',nodes.paragraph(text=f"Page Properties Report ({', '.join(report_field_labels)})"),morecols=columns_number)
    table_head_node_title += title_row

    table_group_node += table_head_node_title
    table_group_node += table_head_node

    # Create the tbody node and add it to the table
    table_body_node = nodes.tbody()
    table_group_node += table_body_node

    # Create the header cells and add them to the header row
    header_row = nodes.row()
    for c_header in columns:
        header_row += nodes.entry('',nodes.paragraph(text=c_header))
    table_head_node += header_row

    # Create rows of data cells with links
    # It was a serious pain to make it work
    for index, row in df_transposed.iterrows():
        row_node = nodes.row()
        table_body_node += row_node
        entry_node = nodes.entry()
        row_node += entry_node
        text_node = nodes.paragraph()
        reference_node = nodes.reference(refuri=index + ".html",text=index)
        text_node += reference_node
        entry_node += text_node

        # Add the rest of the columns
        for item in row[1:]:
            entry_node = nodes.entry()
            row_node += entry_node
            entry_node += nodes.paragraph(text=str(item))

    # uncomment to display the table content during output
    #print(table_node.pformat())
    return table_node

def replace_label_request_nodes_with_doc_refs(app, doctree, docname):  # doctree-resolved | event 14

    all_label_request_nodes = doctree.findall(LabelRequestPlaceholderNode)

    document_to_filtered_data_mapping = app.env.field_data
    label_to_document_mapping = app.env.label_to_document_mapping

    for label_request_placeholder_node in all_label_request_nodes:
        requested_labels = label_request_placeholder_node.requested_labels
        data_table_nodes = create_table_node(document_to_filtered_data_mapping)
#        data_table_nodes = _make_data_table_for_requested_labels(
#            requested_labels,
#            document_to_filtered_data_mapping,
#            label_to_document_mapping,
#        )

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
    #
    # FYI: A reference of the sequence of core events
    #
    # event 04, app.connect("env-before-read-docs", event_04_env_before_read_docs)
    # event 06, app.connect("source-read", event_06_source_read)
    # event 08, app.connect("doctree-read", event_08_doctree_read)
    # event 10, app.connect("env-updated", event_10_env_updated)
    # event 12, app.connect("env-check-consistency", event_12_env_check_consistency)
    # event 14, app.connect("doctree-resolved", event_14_doctree_resolved)

    # the directive
    app.add_directive('page_properties_report', PagePropertiesReport)

    # FYI: when to parse the documents
        # "doctree-read" will process 1 doctree at a time
        # "env-updated" will get me the whole env with

    app.connect('doctree-resolved', replace_label_request_nodes_with_doc_refs) # all doctrees in it
    # i've decided on env-updated to collect the info from the env
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
