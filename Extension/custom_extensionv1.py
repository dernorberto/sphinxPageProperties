from docutils import nodes
from docutils.parsers.rst import directives, Directive


class FieldTableDirective(Directive):
    has_content = False

    def run(self):
        env = self.state.document.settings.env

        # Retrieve all .rst files in the project
        rst_files = env.found_docs

        # Parse fields from each .rst file
        field_data = {}
        for rst_file in rst_files:
            with open(env.doc2path(rst_file), 'r') as file:
                content = file.read()
                fields = parse_fields(content)
                if fields:
                    field_data[rst_file] = fields

        # Generate the table node
        table_node = generate_table(field_data)

        return [table_node]


def parse_fields(content):
    # Implement your logic to parse field keys and values from the content
    # This could involve regular expressions or other parsing techniques
    # Return the extracted field data as a dictionary or list of tuples

    # Example:
    field_data = {'Author': 'John Doe', 'Date': '2023-05-01', 'Version': '1.0'}
    return field_data


def generate_table(field_data):
    # Create a table node
    table_node = nodes.table()

    # Create table column specifications
    tgroup_node = nodes.tgroup(cols=3)
    table_node += tgroup_node
    tgroup_node += nodes.colspec(colwidth=1)
    tgroup_node += nodes.colspec(colwidth=1)
    tgroup_node += nodes.colspec(colwidth=1)

    # Add table header row
    thead_node = nodes.thead()
    row_node = nodes.row()
    row_node += nodes.entry(text='Page')
    row_node += nodes.entry(text='Field')
    row_node += nodes.entry(text='Value')
    thead_node += row_node
    tgroup_node += thead_node

    # Add table body rows for each page's fields
    tbody_node = nodes.tbody()
    for page, fields in field_data.items():
        for key, value in fields.items():
            row_node = nodes.row()
            row_node += nodes.entry(text=page)
            row_node += nodes.entry(text=key)
            row_node += nodes.entry(text=value)
            tbody_node += row_node
    tgroup_node += tbody_node

    return table_node


def setup(app):
    app.add_directive('fieldtable', FieldTableDirective)

    return {'version': '1.0', 'parallel_read_safe': True}