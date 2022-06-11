#!/bin/bash
source /venv/bin/activate
cd /app

echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "-----------Run gunicorn--------- "
gunicorn -b :5000 sila.wsgi:application