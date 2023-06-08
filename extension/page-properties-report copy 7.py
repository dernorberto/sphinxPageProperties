from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective

"""
from ChatGPT
> In a sphinx 6 extension, I need to get data from the "doctree-read" sphinx event then
> pass it to the directive class then put the content where the directive is placed in the rest file
"""
class FieldParser:
    def __init__(self):
        self.fields = {}

    def parse_fields(self, app, doctree):
        for node in doctree.traverse(nodes.field_list):
            print(node)
            field_name = None
            field_value = None

            for field_node in node.children:
                if isinstance(field_node, nodes.field_name):
                    field_name = field_node.astext()
                elif isinstance(field_node, nodes.field_body):
                    field_value = field_node.astext()

            if field_name and field_value:
                self.fields[field_name] = field_value


class PagePropertiesReport(SphinxDirective):
    def run(self):
        field_parser = self.env.app.field_parser

        # Create a paragraph node with the content from field_parser
        para_node = nodes.paragraph()
        para_node += nodes.Text(str(field_parser.fields))

        return [para_node]


def setup(app):
    app.add_directive('pagepropertiesreport', PagePropertiesReport)

    field_parser = FieldParser()
    app.field_parser = field_parser
    app.connect('doctree-read', field_parser.parse_fields)

    return {'version': '1.0', 'parallel_read_safe': True}
