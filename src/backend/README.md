# General Notes and Introduction

*UPDATED 2019-12-24*

This is the backend API/application that power the the Door Unlock Application 
for Pitt RAS. This document outlines the role of the backend API and other general
notes about interacting with this API.

## Purpose of the API

This API provides the backing data and access to the door and management of said
door. This provides the endpoints for both a Slack bot and a local web applica-
tion. Additioanlly, this API is also the central data management service for
verifying and authentication credentials for users to unlock the physical door.

## Technologies Used and Setup

This application is largely a Python app powered by the following:
* Flask
    - Flask-Restful
        * Makes making REST API with Flask easier
    - Flask-SQLAlchemy
        * Object Relational Mapper and Database access
        * Meant to be DB agnostic
    - Flask-Marshmallow
        * For object serialization/deserialization and validation
* SQLite (Used by SQLAlchemy)
    - Lightweight RBDMS (because I don't have a 512 MB to give to a database)
* Docker
    - Containerization and Orchestration tool 

### Setup

To setup the environment it is recommended that one uses ```pipenv``` to setup the
required packages. If one is using Visual Studio Code, one may also elect to use
the Remote (Container) extensions and Docker to setup an isolated dev environment
(Note that this is largely still experimental). It is *strongly* discouraged to
use the requirements.txt and requirements-dev.txt files as they are there for
the Docker images and are not guaranteed to be updated. Said files are generated
using ```pipenv lock -r > requirements.txt``` and ```pipenv lock -d -r >
requirements.txt``` respectively. If you wish to add packages, you *should* use
```pipenv```.

## Architecture and Deployment

### General Info

This API largely follows REST methodologies and follows best practices with in that. This
app itself does not handle the Computer Vision and unlocking of the physical door.
Instead, physical door interaction is handled by a different Python program; the
door program interacts with this API by making HTTP requests to a TCP/IP socket.
(Yes, it's not the best choice, UNIX sockets would be better. Can't you tell
the guy who did this is a Web guy?)

### Testing

This is still largely in progress. REST resources are being determined and 
tests are being created gradually. The test suite is not meant to be
comprehensive, just enough to verify very basic operations. Additionally,
if one is using Docker. one can use use ```(sudo) docker build --tag=
door-unlock-api:latest --target=test .```and then ```docker 
run door-unlock-api:latest``` to  run the test suite instead.

### Deployment

For deployment in production, the intention is to use Docker and Docker Compose.
This hopefully will simplify deployment and integration with CI (this is the
primary reason that the application communicates over IP sockets. Sharing a SQLite
database between containers was uncertain, especially given that concurrent database
access for SQLite is dependent on file locks/synchronization primitives).