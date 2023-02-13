============
Installation
============

At the command line::

    $ pip install {{ cookiecutter.project_slug }}

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv {{ cookiecutter.project_slug }}
    $ pip install {{ cookiecutter.project_slug }}

Or, if you are using pipenv::

    $ pipenv install {{ cookiecutter.project_slug }}

{%- if cookiecutter.project_type == "cli" %}
Or, if you are using pipx::

    $ pipx install {{ cookiecutter.project_slug }}
{% endif %}

