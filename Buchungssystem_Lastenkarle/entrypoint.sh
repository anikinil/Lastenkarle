#!/usr/bin/env bash
set -e

host="db"
port="3306"

echo "Starting test if Database is Ready"
until mysqladmin ping -h"$host" -P"$port" --silent; do
  echo "Waiting for database to be ready..."
  sleep 1
done
echo "Execute migration Command"
python manage.py collectstatic --no-input
python manage.py makemigrations db_model
python manage.py makemigrations api
python manage.py makemigrations PrivacyStatement

python manage.py migrate --no-input
echo "Start Server command"
gunicorn Buchungssystem_Lastenkarle.wsgi:application --bind 0.0.0.0:8000