# my_extension.py

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx


class MyDataCollector:
    def __init__(self):
        self.data = []
        self.env.my_data = []

    def collect_data(self, app, doctree):
        # Implement your logic to collect data from the doctree-read event
        # and store it in the `self.data` list
        self.data.append("object1")
        self.data.append("object2")
        print(self.data)
        pass

class MyDirective(Directive):
    def run(self):
        # Access the collected data from the MyDataCollector instance
        #data_collector = self.state.document.settings.env.my_extension_data_collector
        #collected_data = data_collector.data
        collected_data = ['one', 'two']

        # Create nodes to represent the collected data
        content_nodes = []
        for item in collected_data:
            content_nodes.append(nodes.paragraph(text=item))

        # Return the directive's output
        return content_nodes
        return content_nodes

def setup(app):
    #app.add_event('doctree-read', MyDataCollector.collect_data)
    app.connect('doctree-read', MyDataCollector.collect_data)
#    app.add_config_value('my_extension_data_collector', MyDataCollector(), 'env')
    app.add_directive('pagepropertiesreport', MyDirective)

