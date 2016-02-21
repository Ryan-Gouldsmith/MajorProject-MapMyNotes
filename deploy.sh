#!/bin/bash

if [ "$TRAVIS_BRANCH" == "development"];


ssh ryan@ryangouldsmith.uk "cd project

# clone the repo
git clone git@github.com:Ryan-Gouldsmith/MajorProject-MapMyNotes.git

# go to the project
cd MajorProject-MapMyNotes

# checkout the branch we want to checkout
git checkout development

# install any requirements
pip install requirements.txt

# go to the application directory
cd application "

fi

# start up the server
#python setup.py
