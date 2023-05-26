## Confluence Page Properties feature in Sphinx

### Status

* Concept is WIP.
* This repo is meant to:
  * follow the progress of the idea as I stumble along experiments.
  * share the progress with interested collaborators.

### Introduction

* Page Properties & Page Properties Report are THE power feature in Confluence, it's a bit like AirTables *lite*.
* Some use cases I use PP & PPR extensively for:
  * Vendor Inventory
  * Service Inventory
  * Policies/Standards/Procedures
  * Project Tracking

### Some notes

* we are NOT using metadata, we need to parse the content of the doctree, which means using docutils
* Depending on the data I want to get, either field names or something else, I need to either pick **docutils** or **sphinx**

### Work in progress

* Launch `python3 -i tag-finder.py`
* variables
  * **df** = pandas DataFrame
  * **field_data** = the data put into pandas
  * **children_with_set_tags** = all docs containing '.. tags::'
  * **all_files** = all the files in the current sphinx env


#### Outcome
```
>>> df
             File         Field                Value
0  1-child-03.rst      myAuthor      Norberto Soares
1  1-child-03.rst       myTitle        Child Page 03
2  1-child-03.rst          tags  sphinx, meta, child
3  1-child-03.rst  last_changed           14.04.2023
4  1-child-03.rst      pageType          reportChild
5  1-child-02.rst      myAuthor      Norberto Soares
6  1-child-02.rst       myTitle        Child Page 02
7  1-child-02.rst          tags  sphinx, meta, child
8  1-child-02.rst  last_changed           14.04.2023
9  1-child-02.rst      pageType      reportChild-NOT
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
