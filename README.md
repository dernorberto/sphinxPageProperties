## Confluence Page Properties feature in Sphinx

### TODOs

- [x] Labels to filter by as an argument
- [x] Use only Sphinx API to parse content
- [ ] Turn the script into a Sphinx extension
- [x] Replace RST grid table with list-table
- [x] Test using `.. meta::` instead of field lists
- [ ] Select columns to display as an argument of the directive
- [ ] Display the `my_labels` (or equivalent) field list at bottom of each page.

### Status

* First working concept is ready.
* Clone repo, create venv, install requirements, etc...
* Try with the sample files (`0-report.rst, 1-child-01.rst, etc...`).
* In the file `0-report.rst` set the argument of the directive `.. page_properties_report:: arg1[,arg2,arg3]`
* run Sphinx

### Introduction

* I use Page Properties & Page Properties Report extensively Confluence.
* While moving some of the documents to Sphinx, I wanted the same feature.
* I want it to not have to depend on any additional extension.

### Some research notes:

* How to store (meta)data that I want to use like in a Page Properties macro?
  * field-lists:
    * After some initial issues, these are the simplest to use
      * + no external extension required
      * + part of the docutils rst syntax
  * `.. meta::`:
    * - It requires the meta extension
    * - I was not able to easily parse this information.
    * - It was not part of the docutils doctree.
  * `.. tags::`:
    * - It requires the tags extension.
    * + Displays these as tags on the pages.
* Using the manual tag-finder scripts
  * From the `project` folder, launch `python3 tag-finder.py <label1> <label2>...`
  * It will output a file `page_properties_table.rst` that can then be rendered with `make html`

#### Input & Outcome

* Files:
  * All the ReST files in the current sphinx env.
  * Documents whose field lists match:
    * `page_type` set to `reportChild`
    * `my_labels` matching the arguments
  * the structure is similar to:
* Document containing report:
```
...
.. page_properties_report:: it-policy,child
...
```
  * the arg can be >1 string, comma-separated and without spaces.
* Pages collected as children for the report with matching `my_labels`
```
:my_author: Norberto Soares
:my_title: Child Page 02
:author: Norberto Soares
:my_labels: sphinx, meta, child, it-policy
:last_changed: 14.04.2023
:my_status: inprogress
:my_pagetype: reportChild

PPR CHILD 02
===============================
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

