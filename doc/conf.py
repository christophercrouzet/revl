# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.pardir))


class Mock(object):

    __all__ = []

    def __init__(self, signature, *args, **kwargs):
        self._signature = signature

    def __repr__(self):
        return self._signature

    def __call__(self, *args, **kwargs):
        return Mock('%s()' % (self._signature,))

    def __getattr__(self, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        else:
            return Mock('%s.%s' % (self._signature, name))


MOCK_MODULES = ['maya']
for module in MOCK_MODULES:
    sys.modules[module] = Mock(module)


from datetime import datetime

import revl


# -- General configuration ------------------------------------------------

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'revl'
copyright = u"2016-%i, Christopher Crouzet" % (datetime.utcnow().year,)
author = u"Christopher Crouzet"
version = revl.__version__
release = version
language = None

add_module_names = True
autodoc_member_order = 'bysource'
default_role = 'autolink'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
show_authors = False
todo_include_todos = False

description = (
    "A Python library that helps to benchmark code for Autodesk Maya."
)


# -- Options for HTML output ----------------------------------------------

html_description = description.replace(
    'Autodesk Maya',
    '<a href="http://www.autodesk.com/products/maya">Autodesk Maya</a>')

html_theme = 'alabaster'
html_theme_options = {
    'description': html_description,
    'github_user': 'christophercrouzet',
    'github_repo': 'revl',
    'github_type': 'star',
    'fixed_sidebar': True,
}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'links.html',
        'searchbox.html',
        'donate.html',
    ]
}
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = 'revldoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
    (master_doc, 'revl.tex', u"revl Documentation", author, 'manual'),
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, 'revl', u"revl Documentation", [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (master_doc, 'revl', u"revl Documentation", author, 'revl', description,
     'Miscellaneous'),
]
