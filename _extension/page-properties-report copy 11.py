from sphinx.util.docutils import nodes
#from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

# env = sphinx.environment.BuildEnvironment

report_field_pagetype = 'reportChild'

class PagePropertiesReport(SphinxDirective):

    has_content = True
    required_arguments = 1

    def run(self):
        report_field_labels = self.arguments
        report_docname = self.env.docname
        #print(f"\nArguments \"{self.arguments}\" for directive in document {self.env.docname}\n")
        docs_all = list(self.env.found_docs)

        #field_data = self.env.temp_data.get('field_data', None)
        #field_data = self.state.document.settings.env.custom_data
        #field_data = self.state.document.settings.app.env.custom_data
        #print(f"self.state.document.settings = {dir(self.state.document.settings.env.metadata)}")

        #print(f"field_data = {field_data}")

        #return [nodes.paragraph("", "Hello World.")]
        return [nodes.paragraph("Hello world!")]


def process_docinfo(app: Sphinx, all_docs):
    field_data = {}
    report_field_labels = ['it-policy']
    docname = app.env.docname      # this is OK
    field_metadata = app.env.metadata.get(docname, {})          # get the metadata from docinfo
    #print(f"app.env.metadata.get{field_metadata}")
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
                        print(f"SUCCESS: Found {report_field_labels} and added {docname}'s {field_metadata} to \"field_metadata\"\n")
                    else:
                        print(f"PROCESSING ISSUE: {report_field_labels} not in {docname}'s report_field list: {field_list}\n")
                else:
                    print(f"PROCESSING ISSUE: {docname}'s my_labels not present in field_metadata\n")
            else:
                print(f"PROCESSING ISSUE: {docname}'s my_pagetype does not contain reportChild\n")
        else:
            print(f"PROCESSING ISSUE: {docname}'s my_labels not present in field_metadata\n")

    app.env.custom_data.update[{docname:{}}]
    app.env.custom_data[docname].update(field_metadata)
    print(f"app.env.custom_data = {app.env.custom_data}")
    print(f"app.env.temp_data = {app.env.temp_data}")


    return(field_data)


def setup(app: Sphinx):
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
