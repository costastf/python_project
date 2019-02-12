.. {{ cookiecutter.project_slug }} documentation master file, created by
   sphinx-quickstart on {% now 'local' %}.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {{ cookiecutter.project_slug }}'s documentation!
{% set UNDERLINE = '=' * (cookiecutter.project_slug|length + 28) -%}
{{ UNDERLINE }}

Contents:

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   contributing
   modules
   authors
   history

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

