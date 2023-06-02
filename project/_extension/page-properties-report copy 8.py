from docutils import nodes
from docutils.parsers.rst import directives, Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

logger = logging.getLogger(__name__)

"""
from ChatGPT
> A sphinx 6 extension needs to access the field lists using doctree-read event,
place it in a container and retrieve that data with the custom directive in an rest file

and then:
a sphinx 6 extension, that
1. collects data with the doctree-read and places it in a container
2. the directive retrieves data from that container and displays it on an rst document

"""

data_container = []

class PagePropertiesReport(SphinxDirective):
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        # Retrieve the data from the container and process it
        # Generate the output and return a list of nodes
        #data = data_container[0] if data_container else None
        #print(f"The container contains: {data}")
        print(data_container)
        #para_node = nodes.paragraph(text=data)

        return [nodes.paragraph(text="My Custom Directive")]

def on_doctree_read(app, doctree):
    field_data = {}
    report_field_labels = ['it-policy']
    report_field_pagetype = 'reportChild'
    #print(doctree)
    docname = app.env.docname      # this is OK
    field_metadata = app.env.metadata.get(docname, {})
    #print(f"{docname}:\n{field_metadata}\n")

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
                        #container[docname] = field_metadata
                        #data_container.update({docname:{}})
                        #data_container[docname].update(field_metadata)
                        data_container.append(docname)

                        #logger.info("Data collected: %s", field_metadata)

                        print(f"SUCCESS: Found {report_field_labels} and added {docname}'s {field_metadata} to \"field_metadata\"\n")
#                    else:
#                        print(f"PROCESSING ISSUE: {report_field_labels} not in {docname}'s report_field list: {field_list}\n")
#                else:
#                    print(f"PROCESSING ISSUE: {docname}'s my_labels not present in field_metadata\n")
#            else:
#                print(f"PROCESSING ISSUE: {docname}'s my_pagetype does not contain reportChild\n")
#        else:
#            print(f"PROCESSING ISSUE: {docname}'s my_labels not present in field_metadata\n")

def setup(app):
    app.connect("doctree-read", on_doctree_read)
    app.add_directive("pagepropertiesreport", PagePropertiesReport)
    return {'version': '1.0', 'parallel_read_safe': True}
