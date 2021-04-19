#!/bin/sh

python manage.py flush --no-input
python manage.py migrate upload zero
python manage.py makemigrations
python manage.py migrate
gunicorn appy_django.wsgi:application --bind 0.0.0.0:8000

exec "$@"