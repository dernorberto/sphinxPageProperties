# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Confluence 2 Sphinx'
copyright = '2023, Norberto Soares'
author = 'Norberto Soares'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinxcontrib.itemlist",
              "sphinx.ext.autodoc",
              "sphinx.ext.autosummary",
              "sphinx.ext.viewcode",
              "sphinx.ext.todo",
              "sphinx_tags",
              "sphinx_design"
              ]

templates_path = ['_templates']

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "README.md",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

## sphinx_tags settings
tags_create_tags = True
tags_intro_text = "Tags/Labels"
tags_create_badges = True
#tags_badge_colors = "light"
