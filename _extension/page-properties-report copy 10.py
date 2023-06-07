from docutils import nodes
from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective

class MyExtension:
    def setup(self, app):
        app.connect('doctree-read', self.collect_data)

    def collect_data(self, app, doctree):
        # Collect the required data from the doctree
        data = "Sample data"
        # INFO: self = MyExtension
        # Store the collected data in the Sphinx environment
        app.env.my_extension_data = data
        print(f"app: {app}")
        print(f"app.env: {app.env}")
        print(f"app.env.my_extension_data: {app.env.my_extension_data}")        # SUCCESS, display "sample data"
        self.my_extension_data = data
        print(f"self: {self}")
        print(f"self.my_extension_data: {self.my_extension_data}")              # SUCCESS, display "sample data"

class MyDirective(SphinxDirective):
    def run(self):
        # Access the collected data from the Sphinx environment
        #data = self.env.my_extension_data
        print(f"app: {app}")
        print(f"app.env: {app.env}")

        print(f"class MyDirective self: {self}")
        print(f"class MyDirective self.my_extension_data: {self.my_extension_data}")              # SUCCESS, display "sample data"


        # Generate the directive's output
        data = "bla bla"
        para = nodes.paragraph(text="Collected Data: {}".format(data))

        return [para]

def setup(app):
    app.add_directive('pagepropertiesreport', MyDirective)

    my_extension = MyExtension()
    my_extension.setup(app)
