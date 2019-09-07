# Using Ubuntu 18.04 LTS base image
FROM python:3.7-alpine

LABEL Name="door-unlock-api" Version=0.1.0

RUN apk update && apk add sqlite

RUN pip3 install pipenv

WORKDIR /app

COPY . /app

RUN pipenv install --deploy --system 

CMD python3 app.py
