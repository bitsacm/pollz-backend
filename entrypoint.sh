#!/bin/sh
echo "Making migrations and migrating the database. "

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
echo starting gunicorn
python manage.py runserver 0.0.0.0:8000
