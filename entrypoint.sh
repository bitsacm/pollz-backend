#!/bin/sh
echo "Making migrations and migrating the database."

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "$DJANGO_ENV" = "development" ]; then
    echo "Starting Django dev server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting Gunicorn..."
    gunicorn -c gunicorn_conf.py pollz.wsgi:application --bind 0.0.0.0:8000
fi
