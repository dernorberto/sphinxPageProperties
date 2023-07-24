#from docutils import nodes
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

# env = sphinx.environment.BuildEnvironment

report_field_pagetype = 'reportChild'


class FieldCollector:
    def __init__(self):
        self.fields = []

    def collect_fields(self, app: Sphinx, doctree: nodes.document):
        for node in doctree.traverse(nodes.field):
            field_name = node[0].astext()
            field_value = node[1].astext()
            self.fields.append({'name': field_name, 'value': field_value})


class PagePropertiesReport(SphinxDirective):
    def run(self):
        field_collector = self.env.temp_data.get('field_collector')
        if field_collector:
            field_nodes = []
            for field in field_collector.fields:
                field_nodes.append(nodes.field(name='', names=[nodes.field_name('', field['name'])],
                                               body=[nodes.paragraph('', '', nodes.Text(field['value']))]))
            return field_nodes
        else:
            return []

class oldPagePropertiesReport(SphinxDirective):
    has_content = False
    required_arguments = 1

    def run(self):
        report_field_labels = self.arguments
        report_docname = self.env.docname
        print(f"Arguments \"{self.arguments}\" for directive in document {self.env.docname}")
        docs_all = list(self.env.found_docs)

        #return [nodes.paragraph("", "Hello World.")]
        return [nodes.paragraph(docs_all)]





def setup(app):
    field_collector = FieldCollector()
    app.connect('doctree-read', field_collector.collect_fields)
    app.add_directive('fields', FieldsDirective)
    app.env.temp_data.setdefault('field_collector', field_collector)


def oldsetup(app: Sphinx):
    #app.connect("builder-inited", collect_metadata)             # 2. event.builder-inited(app)
    #app.connect("env-before-read-docs", collect_metadata)       # 4. event.env-before-read-docs(app, env, docnames)

    report_field_labels = 'it-policy'
    #app.connect("doctree-read", process_metadata)
    app.connect("doctree-read", process_docinfo)                # OK! This one actually accesses the docinfo!!!!!, docs say its "event.doctree-read(app, doctree)"
    app.add_directive('pagepropertiesreport', PagePropertiesReport)


    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }