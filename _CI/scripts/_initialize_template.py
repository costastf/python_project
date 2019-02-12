#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: _initialize_template.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

import os
import sys
import logging


# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI._initialize_template'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def add_ci_directory_to_path():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    ci_path = os.path.abspath(os.path.join(current_file_path, '..'))
    if ci_path not in sys.path:
        sys.path.append(ci_path)


def initialize_template_environment():
    from configuration import (LOGGING_LEVEL,
                               ENVIRONMENT_VARIABLES,
                               PREREQUISITES)
    from library import (setup_logging,
                         validate_binary_prerequisites,
                         validate_environment_variable_prerequisites,
                         is_venv_created,
                         execute_command,
                         load_environment_variables,
                         load_dot_env_file,
                         activate_virtual_environment)
    load_environment_variables(ENVIRONMENT_VARIABLES)
    load_dot_env_file()
    if not validate_binary_prerequisites(PREREQUISITES.get('executables', [])):
        LOGGER.error('Prerequisite binary missing, cannot continue.')
        raise SystemExit(1)
    if not validate_environment_variable_prerequisites(PREREQUISITES.get('environment_variables', [])):
        LOGGER.error('Prerequisite environment variable missing, cannot continue.')
        raise SystemExit(1)
    if not is_venv_created():
        LOGGER.debug('Trying to create virtual environment.')
        success = execute_command('pipenv install --dev  --ignore-pipfile')
        if success:
            activate_virtual_environment()
            from emoji import emojize
            LOGGER.info('%s Successfully created virtual environment and loaded it! %s',
                        emojize(':white_heavy_check_mark:'),
                        emojize(':thumbs_up:'))
        else:
            LOGGER.error('Creation of virtual environment failed, cannot continue, '
                         'please clean up .venv directory and try again...')
            raise SystemExit(1)
    setup_logging(os.environ.get('LOGGING_LEVEL') or LOGGING_LEVEL)


def bootstrap_template():
    add_ci_directory_to_path()
    from library import activate_template
    activate_template()
    initialize_template_environment()


bootstrap_template()
