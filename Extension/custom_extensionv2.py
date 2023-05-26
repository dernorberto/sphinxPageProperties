from docutils import nodes
from docutils.parsers.rst import directives, Directive


class ReportChildMetadataTableDirective(Directive):
    has_content = False

    def run(self):
        env = self.state.document.settings.env

        # Retrieve all .rst files in the project
        rst_files = env.found_docs

        # Filter .rst files by "pageType" field with value "reportChild"
        filtered_files = []
        for rst_file in rst_files:
            with open(env.doc2path(rst_file), 'r') as file:
                content = file.read()
                if has_report_child_page_type(content):
                    filtered_files.append(rst_file)

        # Extract metadata from filtered files
        metadata = {}
        for rst_file in filtered_files:
            with open(env.doc2path(rst_file), 'r') as file:
                content = file.read()
                file_metadata = extract_metadata(content)
                metadata[rst_file] = file_metadata

        # Generate the table summarizing common field keys
        common_fields_table = generate_common_fields_table(metadata)

        # Generate the table with field values per file
        field_values_table = generate_field_values_table(metadata)

        return [common_fields_table, field_values_table]


def has_report_child_page_type(content):
    # Implement your logic to check if the "pageType" field has the value "reportChild"
    # This could involve parsing the content and examining the field value
    # Return True if the field has the desired value, False otherwise

    # Example:
    # Assuming the "pageType" field is in the format ":pageType: reportChild"
    return ':pageType: reportChild' in content


def extract_metadata(content):
    # Implement your logic to extract metadata from the content
    # This could involve regular expressions or other parsing techniques
    # Return the extracted metadata as a dictionary

    # Example:
    metadata = {'Title': 'Sample Report', 'Author': 'John Doe', 'Date': '2023-05-01'}
    return metadata


def generate_common_fields_table(metadata):
    # Get the common field keys from all files
    common_keys = set.intersection(*[set(file_metadata.keys()) for file_metadata in metadata.values()])

    # Create a table node for the common fields
    table_node = nodes.table()
    tgroup_node = nodes.tgroup(cols=len(common_keys))
    table_node += tgroup_node

    # Create table column specifications
    for _ in common_keys:
        tgroup_node += nodes.colspec(colwidth=1)

    # Add table header row
    thead_node = nodes.thead()
    row_node = nodes.row()
    for key in common_keys:
        row_node += nodes.entry(text=key)
    thead_node += row_node
    tgroup_node += thead_node

    return table_node


def generate_field_values_table(metadata):
    # Create a table node for field values per file
    table_node = nodes.table()
    tgroup_node = nodes.tgroup(cols=len(metadata) + 1)
    table_node += tgroup_node

    # Create table column specifications
    tgroup_node += nodes.colspec(colwidth=1)
    for _ in metadata:
        tgroup_node += nodes.colspec(colwidth=1)

    # Add table header row
    thead_node = nodes.thead()
    row_node = nodes.row()
    row_node += nodes.entry(text='Page')
    for _ in metadata:
        row_node += nodes.entry(text='Field Value')
    thead_node += row_node
    tgroup_node += thead_node

    # Add table body rows for each file's field values
    tbody_node = nodes.tbody()
    for rst_file, file_metadata in metadata.items():
        row_node = nodes.row()
        row_node += nodes.entry(text=rst_file)
        for value in file_metadata.values():
            row_node += nodes.entry(text=value)
        tbody_node += row_node
    tgroup_node += tbody_node

    return table_node


def setup(app):
    app.add_directive('reportchildmetadata', ReportChildMetadataTableDirective)

    return {'version': '1.0', 'parallel_read_safe': True}
