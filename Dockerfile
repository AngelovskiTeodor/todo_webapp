FROM python:alpine as env

ENV PYTHONUNBUFFERED 1

RUN mkdir /todo_webapp_source
WORKDIR /todo_webapp_source

COPY todo_webapp/* /todo_webapp_source/todo_webapp/
COPY todo_webapp_project/* /todo_webapp_source/todo_webapp_project/
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

#RUN printenv POSTGRES_PASSWORD
#RUN sleep 5

COPY environ_temp.py /todo_webapp_source/
RUN python environ_temp.py

EXPOSE 80
#RUN python manage.py makemigrations todo_webapp
#RUN python manage.py migrate
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
ENTRYPOINT python environ_temp.py && python manage.py makemigrations todo_webapp && python manage.py migrate && python manage.py runserver 0.0.0.0:80
#ENTRYPOINT [ "/bin/ash" ]