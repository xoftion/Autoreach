#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py createadmin
python manage.py collectstatic --noinput
