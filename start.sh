#!/bin/bash

redis-server --daemonize yes --port 6379

celery -A autoreach worker --loglevel=info --detach

celery -A autoreach beat --loglevel=info --detach

sleep 2

gunicorn --bind 0.0.0.0:5000 --workers 2 autoreach.wsgi:application
