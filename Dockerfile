FROM python:3.8.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update

RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential

COPY requirements.txt /

RUN pip install -r requirements.txt 

WORKDIR /django-api/

COPY Pipfile Pipfile.lock /django-api/

RUN pipenv install --system --clear

WORKDIR /django-api/app

COPY ./app .