from docutils import core
from docutils.core import Publisher
from docutils.writers.html5_polyglot import Writer as HTMLWriter

import os

with open('rst_table.txt', encoding='utf-8') as file:
    rst_file = file.read()


# docutils
content_doctree = core.publish_doctree(source=rst_file)
# publish_doctree generates docutils.node.document
content_parts = core.publish_parts(source=rst_file)
# publish_parts generates dict
content_string = core.publish_string(source=rst_file)
# publish_parts generates bytes

#

with open('rst_doctree.html', 'wt') as file:
    file.write(content_doctree.astext())

with open('rst_parts.html', 'wt') as file:
    file.write(str(content_parts))

with open('rst_string.html', 'wt') as file:
    file.write(content_string.decode('utf-8'))

content_publisher = core.publish_parts(rst_file, writer_name='html')
content_publisher_html = content_publisher['html_body']
#publisher.destination = (None,None)
#publisher.writer=HTMLWriter()


with open('rst_publish.html', 'wt') as file:
    file.write(content_publisher_html)
