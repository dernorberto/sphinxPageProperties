from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

report_field_pagetype = 'reportChild'

class PagePropertiesReport(SphinxDirective):

    required_arguments = 1

    def run(self):
        env = self.state.document.settings.env
        field_data = {}

        # Iterate over all documents in the environment
        for docname in env.found_docs:
            # Get the docinfo for the document
            docinfo = env.metadata.get(docname, {})
            print(docinfo)
            if docinfo:
                # Check if the desired value is present in the docinfo
                if self.arguments[0] in docinfo:
                    field_data[docname] = docinfo[self.arguments[0]]

        # Create a nodes.literal_block containing the docinfo dictionary
        docinfo_node = nodes.literal_block(text=str(field_data))
        print(f"field_data = {field_data}")
        print(f"docinfo_node = {docinfo_node}")
        return [docinfo_node]

def process_docinfo(app: Sphinx, doctree):
    report_field_labels = list('it-policy')
    docname = app.env.docname      # this is OK
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
    return [field_metadata]



def setup(app):
    app.connect("doctree-read", process_docinfo)       # OK! This one actually accesses the docinfo!!!!!, docs say its "event.doctree-read(app, doctree)"
    app.add_directive('pagepropertiesreport', PagePropertiesReport)

    return {'version': '1.0'}

