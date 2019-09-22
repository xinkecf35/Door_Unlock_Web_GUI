# Builder/Base State
FROM python:3.7-alpine AS builder
LABEL Name="door-unlock-api" Version=0.1.0
RUN apk update && apk add sqlite
RUN pip3 install pipenv
WORKDIR /app
COPY . /app

#  Deploy stage, no unit tests
FROM builder AS deploy

VOLUME [ "/app/data" ]

RUN pipenv install --deploy --system 

CMD python3 app.py
