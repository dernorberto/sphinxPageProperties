from docutils import nodes
from sphinx.util.docutils import SphinxDirective

# direct copy from chatgpt

class FieldParser:
    def __init__(self):
        self.fields = {}

    def parse_fields(self, app, doctree):
        for node in doctree.traverse(nodes.field_list):
            field_name = None
            field_value = None

            for field_node in node.children:
                if isinstance(field_node, nodes.field_name):
                    field_name = field_node.astext()
                elif isinstance(field_node, nodes.field_body):
                    field_value = field_node.astext()

            if field_name and field_value:
                self.fields[field_name] = field_value
        print(self.fields)


class PagePropertiesReport(SphinxDirective):
    def run(self):
        field_parser = self.env.app.field_parser

        # Create a table node
        table_node = nodes.table()
        tgroup_node = nodes.tgroup(cols=2)
        table_node += tgroup_node

        # Create column specifications
        tgroup_node += nodes.colspec(colwidth=1)
        tgroup_node += nodes.colspec(colwidth=1)

        # Add header row
        thead_node = nodes.thead()
        row_node = nodes.row()
        row_node += nodes.entry(text='Field')
        row_node += nodes.entry(text='Value')
        thead_node += row_node
        tgroup_node += thead_node

        # Add body rows for fields
        tbody_node = nodes.tbody()
        for field_name, field_value in field_parser.fields.items():
            row_node = nodes.row()
            row_node += nodes.entry(text=field_name)
            row_node += nodes.entry(text=field_value)
            tbody_node += row_node
        tgroup_node += tbody_node

        return [table_node]


def setup(app):
    app.add_directive('pagepropertiesreport', PagePropertiesReport)

    field_parser = FieldParser()
    app.field_parser = field_parser
    app.connect('doctree-read', field_parser.parse_fields)

    return {'version': '1.0', 'parallel_read_safe': True}