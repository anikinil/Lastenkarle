#!/usr/bin/env bash
set -e



echo "Execute migration Command"
python manage.py collectstatic --no-input
#python manage.py makemigrations db_model
#python manage.py makemigrations api

python manage.py migrate --no-input
echo "Start Server command"
gunicorn Buchungssystem_Lastenkarle.wsgi:application --bind 0.0.0.0:8000