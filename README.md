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
