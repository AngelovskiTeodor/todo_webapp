FROM python:alpine as env

ENV PYTHONUNBUFFERED 1

RUN mkdir /todo_webapp_source
WORKDIR /todo_webapp_source

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

COPY requirements.txt /todo_webapp_source/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
