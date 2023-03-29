FROM python:3.11-alpine
LABEL maintainer="mplabs.tech"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./requirements-dev.txt /requirements-dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN apk update
RUN pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update unixodbc-dev unixodbc gnupg dirmngr && \
    apk add --update --no-cache libpq-dev gcc && \
    apk add --update --no-cache --virtual .tmp-build-deps curl \
        build-base postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

USER django-user
