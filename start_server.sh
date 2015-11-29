#!/bin/bash
echo "Hello world"
source /home/lils/.pyenv/versions/lils/bin/activate
/home/lils/.pyenv/versions/lils/bin/gunicorn --env DJANGO_SETTINGS_MODULE=lils.settings lils.wsgi -c gunicorn.conf.py
