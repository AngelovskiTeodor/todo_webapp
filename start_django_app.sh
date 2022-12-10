#!/bin/sh
#Warning: End of Line Sequence/Control_Character must be LF instead of CRLF. Git changes LF to CRLF implicitly when adding or committing
echo "Making DB migrations and starting todo_webapp..."
#python manage.py migrate
python manage.py makemigrations todo_webapp
python manage.py migrate
python manage.py runserver 0.0.0.0:80