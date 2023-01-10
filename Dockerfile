FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev icu-data-full

RUN pip install -r /temp/requirements.txt

RUN python -m pip install --upgrade pip

COPY crown /crown

WORKDIR /crown
