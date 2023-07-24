from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

report_field_pagetype = 'reportChild'

class MyDirective(SphinxDirective):
    def run(self):
        # Access the data stored in the environment
        #data = self.env.my_extension_data
        #print(f"MyDirective: data = {data}\n")
        print(f"MyDirective: self.state = {dir(self.state)}\n")
        print(f"MyDirective: self.state.document = {dir(self.state.document)}\n")
        print(f"MyDirective: self.state.document.settings = {dir(self.state.document.settings)}\n")
        print(f"MyDirective: self.state.document.settings.env = {dir(self.state.document.settings.env)}\n")
        print(f"MyDirective: self.state.document.settings.env.found_docs = {self.state.document.settings.env.found_docs}\n")
        print(f"MyDirective: self.state.document.settings.env.metadata = {self.state.document.settings.env.metadata}\n")

        my_data = self.options.get('mydata', self.config.mydata)
        print(f"my_data = {my_data}")
        # Process the data and generate the directive's output
        output = "some data that I collected"

        # Create a paragraph node to hold the output
        para = nodes.paragraph()
        para += nodes.Text(output)

        return [para]

def setup(app):
    app.add_directive('pagepropertiesreport', MyDirective)
    app.connect('doctree-read', process_docinfo)
    app.connect('builder-inited', collect_data)
    app.add_config_value('mydata', '', 'env')

def process_docinfo(app: Sphinx, doctree):
    field_data = {}
    report_field_labels = ['it-policy']
    report_field_pagetype = 'reportChild'


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
                        print(f"docname = {docname}")
                        #app.env.my_extension_data.update({docname:{}})
                        #app.env.my_extension_data[docname].update(field_metadata)


    #print(f"app.env.my_extension_data = {app.env.my_extension_data} = {len(app.env.my_extension_data)} long\n")

def collect_data(app):
    field_data = {}
    report_field_labels = ['it-policy']
    report_field_pagetype = 'reportChild'
    #field_metadata = app.env.metadata.get(docname, {})
    #field_metadata = app.env.metadata.get(docname, {})          # get the metadata from docinfo

    # Collect and process data
    #data = "This is some data"

    # Store the data in the environment



