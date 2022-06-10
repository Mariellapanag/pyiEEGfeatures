# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath(os.path.join('../../src/')))

# -- Project information -----------------------------------------------------

project = 'pyEDFieeg'
copyright = '2022, Mariella Panagiotopoulou'
author = 'Mariella Panagiotopoulou'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# General
extensions = [
    "myst_parser",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx_autodoc_typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    #"sphinx.ext.githubpages",
]

#templates_path = ["_templates"]
#exclude_patterns = ["_build"]

# Napoleon style - custom additions
# Digging through the PR, I found where to look: the napoleon_type_aliases configuration item allows you to set up a mapping for things like array-like, dict-like, etc. In this particular case, adding the following to conf.py did the trick:
# napoleon_use_param has to be True for this to work. It's documented as defaulting to True, but somewhere along the way in my setup, it got unset. It never hurts to be extra safe.

napoleon_use_param = True
napoleon_type_aliases = {
    'array-like': ':term:`array-like <array_like>`',
    'array_like': ':term:`array_like`',
}

# To link to the array_like term on the numpy site, the intersphinx extension must be enabled, and intersphinx_mapping in conf.py must link to numpy:
intersphinx_mapping = {
    'numpy': ('https://numpy.org/doc/stable/', None),

    }
#    'matplotlib': ('https://matplotlib.org/stable/', None),

#myst_url_schemes = ["http", "https", ]

# HTML output
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 2,
}


html_context = {
    "display_github": True,
    "github_user": "Mariellapanag",
    "github_repo": "pyEDFieeg",
    "github_version": "main",
    "last_updated": True,
    "conf_py_path": "../docs/source/", # path in the docs root
    "source_suffix": ".md",
}

html_title = "pyEDFieeg"
html_static_path = ["_static"]
#html_extra_path = ["README.md"]
html_css_files = ["custom.css"]
pygments_style = "friendly"
html_show_sphinx = False