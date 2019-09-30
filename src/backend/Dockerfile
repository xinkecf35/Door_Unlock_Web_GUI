# Builder/Base State
FROM python:3.7-alpine AS builder
LABEL Name="door-unlock-api" Version=0.1.0
RUN apk update && apk add sqlite
RUN pip3 install pipenv
WORKDIR /app
COPY . /app/
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# unit test stage
FROM builder AS test
RUN pipenv lock --requirements --dev > requirements.txt
RUN pip install -r requirements.txt
CMD pytest

#  Deploy stage, no unit tests
FROM builder AS production
VOLUME [ "/app/data" ]
CMD python3 src/app.py
