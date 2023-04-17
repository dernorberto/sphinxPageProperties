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

#              "sphinxcontrib.itemlist",
#              "sphinx.ext.autodoc",
#              "sphinx.ext.autosummary",
#              "sphinx.ext.viewcode",
#              "sphinx.ext.todo",
#              "sphinx_tags",
#              "sphinx_design",
#              "sphinx_needs",
#              "sphinx_needs",

extensions = [
    "sphinx.ext.autodoc",
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
html_theme_options = {              # https://alabaster.readthedocs.io/en/latest/customization.html#theme-options
#    'logo': 'logo.png',
#    'github_user': 'sphinx-doc',
#    'github_repo': 'alabaster',
    'description': 'Norberto trying to replicate Page Properties with Sphinx',
    'logo': 'ACME.jpg',
    'github_user': 'dernorberto'
}
html_additional_pages = {
    'contents': 'contents.html'
}

LANGS = ['en', 'de', 'cn']

# getting to use variables
html_context = {
    'myVariables': len(LANGS)
    }


# Alabaster customized sidebat templates
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}



html_static_path = ['_static']

## sphinx_tags settings
tags_create_tags = True
tags_intro_text = "Tags/Labels"
tags_create_badges = True
#tags_badge_colors = "light"
