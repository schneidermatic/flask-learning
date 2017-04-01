#!/bin/bash


source ./venv/bin/activate
cd ./app
python manage.py runserver --host 0.0.0.0 --port 8080
