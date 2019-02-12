#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tag.py
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
import argparse
import logging

# this sets up everything and MUST be included before any third party module in every step
import _initialize_template

from bootstrap import bootstrap
from gitwrapperlib import Git
from library import bump
from configuration import BRANCHES_SUPPORTED_FOR_TAG

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.tag'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def check_branch():
    git = Git()
    if git.get_current_branch() not in BRANCHES_SUPPORTED_FOR_TAG:
        accepted_branches = ', '.join(BRANCHES_SUPPORTED_FOR_TAG)
        print(f'Tagging is only supported on {accepted_branches} '
              'you should not tag any other branch, exiting!')
        raise SystemExit(1)


def filter_patch(patch):
    patch = patch.replace('\ndiff', '\n|||diff')
    return r''.join([line for line in patch.split('|||')
                     if '{{cookiecutter.project_slug}}' in line])


def create_patch(old_version, new_version):
    git = Git()
    patch = git.create_patch(old_version, new_version)
    patch = filter_patch(patch)
    patch_file = os.path.join('{{cookiecutter.project_slug}}',
                              '_CI',
                              'patches',
                              f'{new_version}.patch')
    with open(patch_file, 'w') as ofile:
        ofile.write(patch)
    return patch_file


def get_arguments():
    parser = argparse.ArgumentParser(description='Handles bumping of the artifact version')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--major', help='Bump the major version', action='store_true')
    group.add_argument('--minor', help='Bump the minor version', action='store_true')
    group.add_argument('--patch', help='Bump the patch version', action='store_true')
    args = parser.parse_args()
    return args


def commit_patch_and_push(segment, current_version, version_file_path):
    git = Git()
    new_version = bump(segment, version_file_path)
    print(f'Commiting version {new_version}')
    git.commit(f'Set version to {new_version}', version_file_path)
    print(f'Tagging version {new_version}')
    git.add_tag(new_version)
    print(f'Creating patch between version {current_version} and {new_version}')
    patch_file = create_patch(current_version, new_version)
    print(f'Adding file {patch_file} to git tracking')
    git.add(patch_file)
    print(f'Commiting {patch_file}')
    git.commit(f'Adding patch file for version "{new_version}"', patch_file)
    print('Pushing everything')
    git.push()
    print(f'Pushing tag {new_version}')
    git.push('origin', new_version)
    return new_version


def tag(segment):
    bootstrap()
    check_branch()
    version_file_path = os.path.join('{{cookiecutter.project_slug}}', '_CI', '.VERSION')
    current_version = open(version_file_path).read().strip()
    if segment:
        version = commit_patch_and_push(segment, current_version, version_file_path)
    else:
        version = bump(segment, version_file_path)
    print(version)
    raise SystemExit(0)


if __name__ == '__main__':
    args = get_arguments()
    segment = next((argument for argument in ('major', 'minor', 'patch')
                    if getattr(args, argument)), None)
    tag(segment)
