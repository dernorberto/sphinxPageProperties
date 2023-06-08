from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

logger = logging.getLogger(__name__)

"""
chatgpt:
> In a sphinx 6 extension, I need to get data from the "doctree-read" sphinx event then p
ass it to the directive class then put the content where the directive is placed in the rest file
"""

class FieldParser:
    def __init__(self):
        self.fields = {}

    def parse_fields(self, app, doctree):
        report_field_labels = ['it-policy']
        report_field_pagetype = 'reportChild'
        field_data = {}

        docname = app.env.docname
        field_metadata = app.env.metadata.get(docname, {})

        if field_metadata != {}:
            if 'my_pagetype' in field_metadata:
                if report_field_pagetype in field_metadata['my_pagetype']:
                    if 'my_labels' in field_metadata:
                        field_list = field_metadata['my_labels'].split(', ')
                        # check if all elements of report_field_labels are in field_list
                        if all(element in field_list for element in report_field_labels):
                            # if True, then add to field_data
                            field_data.update({docname:{}})
                            field_data[docname].update(field_metadata)
                            self.fields.update({docname:{}})
                            self.fields[docname].update(field_metadata)
                            #logger.info("Data collected: %s", field_metadata)
    def run():
        return(self.fields)

class PagePropertiesReport(SphinxDirective):
    def run(self):
        field_parser = self.env.app.field_parser

        # Create a paragraph node with the content from field_parser
        para_node = nodes.paragraph()
        para_node += nodes.Text(str(field_parser.fields))
        logger.info("para_node: %s", type(field_parser.fields))

        return [para_node]


def setup(app):
    app.add_directive("pagepropertiesreport", PagePropertiesReport)

    field_parser = FieldParser()
    app.field_parser = field_parser
    app.connect('doctree-read', field_parser.parse_fields)

    return {'version': '1.0', 'parallel_read_safe': True}
