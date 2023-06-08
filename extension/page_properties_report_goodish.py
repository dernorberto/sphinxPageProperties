#from docutils import nodes
from sphinx.util.docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

# env = sphinx.environment.BuildEnvironment

report_field_pagetype = 'reportChild'
field_data = {}
report_field_labels = ['it-policy']

class PagePropertiesReport(SphinxDirective):

    has_content = True
    required_arguments = 1
    def run(self):
        report_field_labels = self.arguments
        report_docname = self.env.docname

        #return [nodes.paragraph("", "[ I want this paragraph to be the Page Properties Report ]")]
        return [nodes.paragraph("", docname)]


def collect_metadata(app: Sphinx):
    metadata = {}  # Dictionary to store collected metadata

    #field_lists = self.env.metadata[doc_path].get("field_lists", [])
    field_metadata = app.env.metadata['1-child-03']
    #print(f"field_metadata = {field_metadata}")

    metadata = app.env.metadata.get('1-child-03')
    #print(f"metadata = {metadata}")

    #for docname, doctree in app.env.found_docs():
    #    metadata[docname] = doctree.settings.env.metadata[docname]

    #app.metadata = metadata  # Store the collected metadata in the app
    return [metadata]

def process_metadata(app, env):
    field_metadata = app.env.metadata.get(app.env.docname, {})          # get the metadata from docinfo
    print(f"process_metadata.field_metadata: {field_metadata}")


def process_docinfo(app: Sphinx, doctree):
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
                        print(docname)
                        #field_data.update({docname:{}})
                        #field_data[docname].update(field_metadata)
                    else:
                        print(f"{docname}'s report_field list: {field_list}")
                else:
                    print(f"{docname}'s my_labels not present in field_metadata")
            else:
                print(f"{docname}'s my_pagetype does not contain reportChild")
        else:
            print(f"{docname}'s my_labels not present in field_metadata")



def setup(app: Sphinx):
    app.add_directive('pagepropertiesreport', PagePropertiesReport)


    #app.connect("builder-inited", collect_metadata)             # 2. event.builder-inited(app)
 #   app.connect("env-before-read-docs", collect_metadata)       # 4. event.env-before-read-docs(app, env, docnames)
    #app.connect("doctree-read", process_metadata)                #
    app.connect("doctree-read", process_docinfo)                # OK! This one actually accesses the docinfo!!!!!, docs say its "event.doctree-read(app, doctree)"


    return {
        'version': '1.0',
        'parallel_read_safe': False,
        'parallel_write_safe': False,
        }
