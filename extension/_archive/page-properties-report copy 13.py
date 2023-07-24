from docutils import nodes
from sphinx.util.docutils import SphinxDirective

class MyExtension:
    def setup(self, app):
        app.connect('doctree-read', self.extract_metadata)

    def extract_metadata(self, app, doctree):
        # Access the metadata from the doctree
        metadata = {
            'key1': 'value1',
            'key2': 'value2',
            # Add more metadata as needed
        }
        #print(f"{metadata}")

        # Store the metadata in the Sphinx environment
        #app.env.metadata[docname] = metadata
#        print(f"app = {app}\n")
#        print(f"app = {dir(app)}\n")
#        print(f"app.env = {app.env}\n")
#        print(f"app.env = {dir(app.env)}\n")
        #print(f"app.env.metadata = {app.env.metadata}\n")
        #print(f"dir(app.env.metadata) = {dir(app.env.metadata)}\n")
        app.env.metadata = metadata
        return[metadata]

class MyDirective(SphinxDirective):
    def run(self):
        # Retrieve the metadata from the Sphinx environment
        metadata = self.env.metadata
        #metadata = self.env.metadata.get(self.env.docname, {})
        extension_data = MyExtension()
        print(dir(extension_data))
        #print(f"MyExtension.extract_metadata = {MyExtension.extract_metadata}")
        print(f"dir(MyExtension.extract_metadata) = {dir(MyExtension.extract_metadata)}")
        # Generate the directive's output using the metadata
        para = nodes.paragraph(text="Metadata: {}".format(metadata))
        return [para]

def setup(app):
    app.add_directive('pagepropertiesreport', MyDirective)
    my_extension = MyExtension()
    my_data = my_extension.setup(app)
    #app.connect('doctree-read', MyExtension.extract_metadata)

