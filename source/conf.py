import sys
sys.path.append('extension')

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Confluence 2 Sphinx'
copyright = '2023, Norberto Soares'
author = 'Norberto Soares'

extensions = [
    'sphinx.ext.autodoc',
    'page_properties_report',
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
#html_theme = 'pydata_sphinx_theme'
#html_theme = 'classic'
#html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "github_user": "optile",
    "github_repo": "tech-docs",
    "github_button": True,
    "github_banner": True,
    "extra_nav_links": {
        "GitHub": "https://github.com/optile/tech-docs/",
    },
}

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

# Alabaster customized sidebar templates
#html_sidebars = {
#    '**': [
#        'about.html',
#        'navigation.html',
#        'relations.html',
#        'searchbox.html',
#        'donate.html',
#    ]
#}

html_static_path = ['_static']
