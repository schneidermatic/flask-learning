#!/bin/bash

find . -name '.project' -delete
find . -name '.pydevproject' -delete
find . -name '*.pyc' -delete
find . -name '*.pyc' -delete
find . -name '*.jpg' -delete
find . -name '*.gif' -delete
rm -rf `find . -name 'migrations'`
rm -rf `find . -name 'venv'`
