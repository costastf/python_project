Python Project Creator
======================

Cookiecutter template for a Python library or cli  project. 


Development/Usage Requirements
------------------------

These utilities / libraries are needed to start developing on or using this template.

 * make
 * cookiecutter
 * pipenv
 * setuptools
 * git


Usage
-----

This template needs to be interpolated with the required variables. This is done through cookiecutter.

    $ cookiecutter python_project
    
This will produce a wizard that will walk through all the required fields and once all questions are answered there will be a project directory in the current directory.

Pipelines all the way down
==========================

This template is provided with it's own CI component. The part of the code residing in the "{{cookiecutter.project_slug}}" is the part of the template to create a new project.

The _CI directory in the root of this project is the CI component for the template itself and provides a few very handy features.

The CI components supports a test command under scripts that can actually cookiecutter the templated part of the code and execute it's internal workflow commands like lint test build and document so any change on that part can be done with confidence since testing that everything still works is very easy.

The idea behind a template is that by initially interpolating it the commands provided should execute without error.
So if any part of the cookiecutter gets changed actually interpolating it and making sure that nothing broke on the execution is crucial.

The external CI components provides the test command to facilitate that testing in an easy manner. So whenever there is any change on the cookiecutter portion executing _CI/scripts/test.py with the appropriate arguments to test will check for us that, that portion still works properly end to end.

**Supported commands** 

    usage: test.py [-h] [--type {lib,cli,all}]
                   (--lint | --test | --build | --document | --all)
    
    Accepts stages for testing
    
    optional arguments:
      -h, --help            show this help message and exit
      --type {lib,cli,all}  The type of template to test ([lib|cli|all]. Default
                            choice is "all")
      --lint                Test the lint stage of the template
      --test                Test the test stage of the template
      --build               Test the build stage of the template
      --document            Test the document stage of the template
      --all                 Test all the stages in the same virtual env



    # interpolates the template in a temp dir and executes the internal lint command and reports on the outcome
    _test --type=(lib|cli|all) --lint
 
     # interpolates the template in a temp dir and executes the internal test command and reports on the outcome
    _test --type=(lib|cli|all) --test
    
     # interpolates the template in a temp dir and executes the internal build command and reports on the outcome
    _test --type=(lib|cli|all) --build
 
     # interpolates the template in a temp dir and executes the internal document command and reports on the outcome
    _test --type=(lib|cli|all) --document
    
    # interpolates the template for both projects and executes all stages in the same virtual environment for speed 
    _test --type=all --all
    
Tagging the code through the _tag command will bump the internal version of the cookiecutter portion of the template and create a git diff patch with the newly created tag so any project created with this template can update itself through the use of that patch by placing it in it's patches directory under it's own _CI directory and executing the update.py command under scripts or just _update if the helper files have been sourced.
