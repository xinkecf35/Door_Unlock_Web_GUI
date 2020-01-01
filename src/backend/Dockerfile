# Builder/Base State
FROM python:3.7-alpine AS builder
LABEL Name="door-unlock-api" Version=0.1.0
RUN apk update && apk add sqlite
RUN pip3 install pipenv
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# unit test stage
FROM builder AS test
RUN pip install -r requirements-dev.txt
CMD pytest

#  Deploy stage, no unit tests
FROM builder AS production
RUN rm -rf Pipfile* requirements*.txt tests
VOLUME [ "/app/data" ]
CMD python3 door_api/app.py
