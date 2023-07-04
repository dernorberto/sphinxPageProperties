#from docutils import nodes
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

""" STATUS OF THIS FILE AS OF 3-Jul-2023

DOING
=====
* parsing all .rst field_list
* collecting all labels based on a hard-coded example of the field to filter by
* placing the labels inside the field "field_data"
* the content of the variable "field_data" for when it's being rendered.

NOT DOING
=========
* collecting the directive argument to use for the filter
* placing the content of the storage node instead of the directive

"""

report_field_pagetype = 'reportChild'
field_data = {}
report_field_labels = ['it-policy']

# my very simple and initial attempt at setting up a node to store data
class StorageNode(nodes.Element):
    pass

class PagePropertiesReport(SphinxDirective):
    has_content = True
    required_arguments = 1

    def run(self):
        report_field_labels = self.arguments

        # I want to replace this below with the content I stored in storage_node
        paragraph_node = nodes.paragraph(text=f"All docs: {self.env.found_docs}\n")
        return [paragraph_node]

    def __repr__(self):
        return str(self.val)

def get_docinfo_from_env(app, env):
    storage_node = StorageNode()
    for n,m in env.metadata.items():
        if 'my_pagetype' in m and 'my_labels' in m:
            if report_field_pagetype in m['my_pagetype']:
                field_list = m['my_labels'].split(', ')
                if all(element in field_list for element in report_field_labels):
                    # if True, then add to field_data
                    field_data.update({n:{}})
                    field_data[n].update(m)
    storage_node.field_data = field_data
    env.storage_node = storage_node

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
    app.connect("env-before-read-docs", event_04_env_before_read_docs)             # event 04
    app.connect("source-read", event_06_source_read)             # event 06
    app.connect("doctree-read", event_08_doctree_read)             # event 08
    app.connect("env-updated", event_10_env_updated)             # event 10
    app.connect("env-check-consistency", event_12_env_check_consistency)             # event 12
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
        # env-updated will get me the whole env with all doctrees in it
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
