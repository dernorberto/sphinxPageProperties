from docutils import nodes
from docutils.parsers.rst import directives, Directive


class ReportChildFileListDirective(Directive):
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

        # Create a bullet list node to display the filtered files
        bullet_list_node = nodes.bullet_list()
        for rst_file in filtered_files:
            list_item_node = nodes.list_item()
            paragraph_node = nodes.paragraph()
            paragraph_node += nodes.Text(rst_file)
            list_item_node += paragraph_node
            bullet_list_node += list_item_node

        return [bullet_list_node]


def has_report_child_page_type(content):
    # Implement your logic to check if the "pageType" field has the value "reportChild"
    # This could involve parsing the content and examining the field value
    # Return True if the field has the desired value, False otherwise

    # Example:
    # Assuming the "pageType" field is in the format ":pageType: reportChild"
    return ':pageType: reportChild' in content


def setup(app):
    app.add_directive('reportchildfilelist', ReportChildFileListDirective)

    return {'version': '1.0', 'parallel_read_safe': True}
