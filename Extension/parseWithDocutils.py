import os
from docutils.core import publish_doctree
from docutils.io import StringInput, NullOutput

src_path = 'example.rst'
src_path = '0-report.rst'

with open(src_path, 'r') as src_file:
    src = src_file.read()

doc = publish_doctree(src, src_path,)
print(doc.pformat())

"""
<document source="0-report.rst">
    <docinfo>
        <author>
            Norberto Soares
        <field classes="myauthor">
            <field_name>
                myAuthor
            <field_body>
                <paragraph>
                    Norberto Soares
...
        <field classes="pagetype">
            <field_name>
                pageType
            <field_body>
                <paragraph>
                    reportParent
...
"""