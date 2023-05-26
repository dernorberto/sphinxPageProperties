import sys
sys.path.append('../Extension')


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
    'sphinx.ext.autodoc',
#    'sphinx_gitstamp',
    'sphinx_tags',
    'sphinx_design',
    'custom_extensionv2',
    'custom_extensionv3',
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
html_theme = 'pydata_sphinx_theme'
html_theme = 'classic'
html_theme = 'sphinx_rtd_theme'
html_theme_options = {              # https://alabaster.readthedocs.io/en/latest/customization.html#theme-options
#    'logo': 'logo.png',
#    'github_user': 'sphinx-doc',
#    'github_repo': 'alabaster',
#    'description': 'Norberto trying to replicate Page Properties with Sphinx',
#    'logo': 'ACME.jpg',
#    'github_user': 'dernorberto'
#    "navbar_start": ["navbar-logo", "version"],
}

html_css_files = [
    'css/page.css',
]


html_additional_pages = {
#    'contents': 'contents.html'
}

LANGS = ['en', 'de', 'cn']

# getting to use variables
html_context = {
    'myVariables': len(LANGS)
    }


# Alabaster customized sidebar templates
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

#variables_to_export = [
#    "myAuthor",
#    "myTitle",
#    "myVariableAbove",
#    "myVariableBelow",
#]

# Date format for git timestamps
gitstamp_fmt = "%b %d, %Y"

# tags extension
tags_overview_title = "Site tags"
tags_create_tags = True
tags_create_badges = True
