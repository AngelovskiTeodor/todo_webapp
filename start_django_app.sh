#!/bin/sh
echo "Making DB migrations and starting todo_webapp..."
python manage.py makemigrations todo_webapp
python manage.py migrate
python manage.py runserver 0.0.0.0:80