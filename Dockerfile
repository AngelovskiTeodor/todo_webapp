FROM todo_base_img:latest as base_env

ENV PYTHONUNBUFFERED 1

COPY todo_webapp/* /todo_webapp_source/todo_webapp/
COPY todo_webapp_project/* /todo_webapp_source/todo_webapp_project/
COPY users/* /todo_webapp_source/users/
COPY manage.py /todo_webapp_source/

EXPOSE 80
COPY start_django_app.sh /todo_webapp_source/
RUN chmod +x start_django_app.sh
ENTRYPOINT [ "sh", "/todo_webapp_source/start_django_app.sh" ]
