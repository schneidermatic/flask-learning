#!/bin/bash

python ./app/manage.py db init
python ./app/manage.py db migrate
python ./app/manage.py db upgrade
