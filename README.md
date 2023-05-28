## Confluence Page Properties feature in Sphinx

### TODOs
* It needs to be an extension that I can call from the page properties report rst file

### Status

* It generates a table based on the field lists from different rst files
* The items in the `my_title` column will be linked to the corresponding HTML file
* v3: `field-finder.py <label> <label> etc...`: using sphinx to get field lists
* v2: `tag-finder.py`: using docutils to get sphinx-tags
* v1: `field-finder-docutils.py`: using docutils to get field lists

### Introduction

* This repo is meant to:
  * follow the progress of the idea as I stumble along experiments.
  * share the progress with interested collaborators.
* Page Properties & Page Properties Report are THE power feature in Confluence, it's a bit like AirTables *lite*.
* Some use cases I use PP & PPR extensively for:
  * Vendor Inventory
  * Service Inventory
  * Policies/Standards/Procedures
  * Project Tracking

### Some notes

* we are NOT using metadata, we need to parse the content of the doctree, which means using docutils
* Depending on the data I want to get, either field names or something else, I need to either pick **docutils** or **sphinx**

### HOWTO

* From the `project` folder, launch `python3 -i tag-finder.py`
* It will output a file `page_properties_table.rst` that can then be rendered with `make html`

#### Input & Outcome

* Input
  * All the ReST files in the current sphinx project.
  * Will select only those with:
    * field list `page_type` set to `reportChild`
    * field list `labels` matching the arguments
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

### Diagram

```
***********************
## Summary-page-01

Properties Report
-----------------
|===============|============|========|========|
| Title         | Approved   | owner  | status |
|===============|============|========|========|
| Child-page-01 | YES        | john   | active |
|---------------|------------|--------|--------|
| Child-page-02 | YES        | mary   | draft  |
|---------------|------------|--------|--------|
| Child-page-03 | NO         | john   | draft  |
|---------------|------------|--------|--------|

***********************


***********************
## Child-page-01

Properties
----------
||----------||--------|
|| Approved || YES    |
||----------||--------|
|| owner    || john   |
||----------||--------|
|| status   || active |
||----------||--------|

***********************


***********************
## Child-page-02

Properties
----------
||----------||--------|
|| Approved || YES    |
||----------||--------|
|| owner    || mary   |
||----------||--------|
|| status   || draft  |
||----------||--------|

***********************

***********************
## Child-page-03

Properties
----------
||----------||--------|
|| Approved || NO     |
||----------||--------|
|| owner    || john   |
||----------||--------|
|| status   || draft  |
||----------||--------|

***********************
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

### Reference Content

* html template to specific document: https://stackoverflow.com/questions/13209597/override-html-page-template-for-a-specific-sphinx-document
* sphinx-tags extension: https://github.com/melissawm/sphinx-tags
  * https://sphinx-tags.readthedocs.io/en/latest/quickstart.html#usage
* metadata: https://docutils.sourceforge.io/docs/ref/rst/directives.html#metadata
* attributes vs fields: http://sphinxsearch.com/forum/view.html?id=9540
* Sphinx templating primer: https://www.sphinx-doc.org/en/master/development/templating.html#jinja-sphinx-templating-primer
* variables: https://stackoverflow.com/questions/14774603/sphinx-add-custom-field-variable-to-be-used-in-html-template
