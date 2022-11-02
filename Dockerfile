FROM python:alpine as env

ENV PYTHONUNBUFFERED 1

RUN mkdir /todo_webapp_source
WORKDIR /todo_webapp_source

COPY todo_webapp/* /todo_webapp_source/todo_webapp/
COPY todo_webapp_project/* /todo_webapp_source/todo_webapp_project/
COPY users/* /todo_webapp_source/users/
COPY manage.py /todo_webapp_source/
COPY requirements.txt /todo_webapp_source/

RUN apk update
RUN apk update && apk upgrade
RUN apk add --no-cache bash\
                       pkgconfig \
                       git \
                       gcc \
                       openldap \
                       libcurl \
                       python3-dev \
                       libpq-dev \
                       gpgme-dev \
                       libc-dev \
    && rm -rf /var/cache/apk/*

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
COPY start_django_app.sh /todo_webapp_source/
RUN chmod +x start_django_app.sh
ENTRYPOINT [ "sh", "/todo_webapp_source/start_django_app.sh" ]