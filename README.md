## Confluence Page Properties feature in Sphinx

### TODOs

- [x] Labels to filter by as an argument
- [x] Use only Sphinx API to parse content
- [ ] Turn the script into a Sphinx extension
- [ ] Replace RST grid table with list-table
- [ ] Test using `.. meta::` instead of field lists

### Status

* It generates an RST grid-table based on the field lists from different rst files
* The items in the `my_title` column will be linked to the corresponding HTML file
* v3: `field-finder.py <label> <label> etc...`: using sphinx to get field lists
* v2: `tag-finder.py`: using docutils to get sphinx-tags
* v1: `field-finder-docutils.py`: using docutils to get field lists

### Introduction

* I use Page Properties & Page Properties Report extensively Confluence.
* While moving some of the documents to Sphinx, I want the same feature.
* I want it to not have to depend on any additional extension.

### Some notes about:

* field-lists:
  * Initially used docutils for parsing, but it was too complex.
  * Currently using Sphinx `<app>.build(False)` and then `<app>.env.metadata` to parse.
* `.. meta::`:
  * I was not able to easily parse this information.
  * It was not part of the docutils doctree.
* `.. tags::`:
  * I ended up not wanting to rely on an extension, although it replicates the Confluence labels feature nicely.

### HOWTO

* From the `project` folder, launch `python3 tag-finder.py <label1> <label2>...`
* It will output a file `page_properties_table.rst` that can then be rendered with `make html`

#### Input & Outcome

* Input
  * All the ReST files in the current sphinx env.
  * Documents whose field lists match:
    * `page_type` set to `reportChild`
    * `labels` matching the arguments
  * the structure is similar to:

```
:my_author: Norberto Soares
:my_title: Child Page 02
:author: Norberto Soares
:my_labels: sphinx, meta, child
:last_changed: 14.04.2023
:my_status: inprogress
:my_pagetype: reportChild-NOT

.. tags:: typeReportChild, PageProperties

PPR CHILD 02
===============================
```


* Output
```
Page Properties Table
===========================

+------------------+-----------------+-----------------+---------------------+--------------+
|     my_title     |  my_pagetype    |     my_author   |         tags        | last_changed |
+==================+=================+=================+=====================+==============+
| `Child Page 03`_ | reportChild     | Norberto Soares | sphinx, meta, child | 14.04.2023   |
+------------------+-----------------+-----------------+---------------------+--------------+
| `Child Page 02`_ | reportChild-NOT | Norberto Soares | sphinx, meta, child | 14.04.2023   |
+------------------+-----------------+-----------------+---------------------+--------------+

.. _Child Page 03: 1-child-03.html
.. _Child Page 02: 1-child-02.html
```


### Experience being replicated

* For simplicity sake:
  * One Parent page that will be used to summarize data from Children pages in a table, ie. Page Properties Report.
  * The data being summarized is a key-value pair added to each Child page, ie. Page Properties.
  * The selection of which pages to include in the PPR is one or more page Labels.

### Features to replicate

* Page Properties
  * key-value pairs added to each child page
* Page Labels
  * This allows filtering which pages include in report.
* Page Properties Report
  * Mechanism to display in a table format, the key-value pairs of the filtered child pages.

