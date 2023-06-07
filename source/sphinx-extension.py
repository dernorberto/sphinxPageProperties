from sphinx.application import Sphinx
import pandas as pd
import os
import argparse
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx


# Order:
#
# 1. parse all open docs
# 2. collect all fields
# 3.
# 4.

# handling arguments
parser = argparse.ArgumentParser()
parser.add_argument('labels',
                    nargs='+',
                    help="1 or more labels to use as a filter")

args = parser.parse_args()
if not args.labels:
    report_field_labels = 'it-policy'
else:
    report_field_labels = args.labels

# other variables
report_field_pagetype = 'reportChild'
report_columns = ['my_title','my_status','last_changed']


class PagePropertiesReport(SphinxDirective):

    def run(self):
        report_field_labels = self.arguments
        report_docname = self.env.docname

        current_dir = os.getcwd()
        source_dir = current_dir
        build_dir = os.path.join(current_dir,'_build')
        doctree_dir = os.path.join(current_dir,'_doctrees')
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


        return [nodes.paragraph("", "[ I want this paragraph to be the Page Properties Report ]")]


class FieldCollector:
    def __init__(self):
        self.fields = []

    def collect_fields(self, app: Sphinx, doctree: nodes.document):
        for node in doctree.traverse(nodes.field):
            field_name = node[0].astext()
            field_value = node[1].astext()
            self.fields.append({'name': field_name, 'value': field_value})
    def collect_fields(self):
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


def setup(app):
    app.connect('doctree-read', field_collector.collect_fields)
    app.add_directive('fields', FieldsDirective)
