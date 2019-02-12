#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: test.py
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

import argparse
import logging
import json
import os

# this sets up everything and MUST be included before any third party module in every step
import _initialize_template

from cookiecutter.main import cookiecutter
from emoji import emojize
from bootstrap import bootstrap
from library import execute_command, tempdir

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.test'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


ALL_TEST_TYPES = ['lib', 'cli']
ALL_STAGES = ['lint', 'test', 'build', 'document']


def get_arguments():
    parser = argparse.ArgumentParser(description='Accepts stages for testing')
    parser.add_argument('--type',
                        choices=['lib', 'cli', 'all'],
                        action='store',
                        help='The type of template to test ([lib|cli|all]. Default choice is "all")',
                        default='all',
                        type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--lint', help='Test the lint stage of the template', action='store_true')
    group.add_argument('--test', help='Test the test stage of the template', action='store_true')
    group.add_argument('--build', help='Test the build stage of the template', action='store_true')
    group.add_argument('--document', help='Test the document stage of the template', action='store_true')
    group.add_argument('--all', help='Test all the stages in the same virtual env', action='store_true')
    args = parser.parse_args()
    return args


def _test(type_, stage):
    template = os.path.abspath('.')
    context_file = os.path.abspath('cookiecutter.json')
    context = json.loads(open(context_file).read())
    test_types = ALL_TEST_TYPES if type_ == 'all' else [type_]
    test_stages = ALL_STAGES if stage == 'all' else [stage]
    result = {}
    status = True
    for test_type in test_types:
        context['project_type'] = test_type
        LOGGER.info('%s Executing testing for template "%s" for stages "%s"! %s',
                    emojize(':fire:'),
                    test_type,
                    test_stages,
                    emojize(':fire:'))
        with tempdir():
            cookiecutter(template,
                         extra_context=context,
                         no_input=True)
            os.chdir(os.listdir('.')[0])
            try:
                del os.environ['PIPENV_PIPFILE']
            except KeyError:
                pass
            result[test_type] = [execute_command(os.path.join('_CI', 'scripts', f'{command}.py'))
                                 for command in test_stages]
    for type_, results in result.items():
        for success, stage in zip(results, test_stages):
            if not success:
                status = False
                LOGGER.error('%s Errors found testing stage "%s" for template type "%s"! %s',
                             emojize(':cross_mark:'),
                             stage,
                             type_,
                             emojize(':crying_face:'))
    return status


def test(type_, stage):
    bootstrap()
    success = _test(type_, stage)
    if success:
        LOGGER.info('%s Tested template type "%s" for stage "%s" successfully! %s',
                    emojize(':white_heavy_check_mark:'),
                    type_,
                    stage,
                    emojize(':thumbs_up:'))
    else:
        LOGGER.error('%s Errors found testing template type "%s" for stage "%s"! %s',
                     emojize(':cross_mark:'),
                     type_,
                     stage,
                     emojize(':crying_face:'))
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    args = get_arguments()
    stage = next((argument for argument in ALL_STAGES
                  if getattr(args, argument)), 'all')
    test(args.type, stage)
