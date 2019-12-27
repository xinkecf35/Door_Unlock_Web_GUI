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
    - Flask-SQLAlchemy
        * Object Relational Mapper and Database access
        * Meant to be DB agnostic
    - Flask-Marshmallow
        * For object serialization/deserialization and validation
* SQLite (Used by SQLAlchemy)
    - Lightweight RBDMS (because I don't have 512 MB to give to a database)
* Docker
    - Containerization and Orchestration tool 

### Setup

To setup the environment it is recommended that one uses ```pipenv``` to setup the
required packages. If one is using Visual Studio Code, one may also elect to use
the Remote (Container) extensions and Docker to setup an isolated dev environment
(Note that this is largely still experimental). It is *strongly* discouraged to
use the requirements.txt and requirements-dev.txt files as they are there for
the Docker images and are not guaranteed to be updated. Said files are generated
using ```pipenv lock -r > requirements.txt``` and
```pipenv lock -d -r >requirements.txt``` respectively. If you wish to add packages,
 you *should* use ```pipenv```.

## Architecture and Deployment

### General Info

This API largely follows REST methodologies and follows best practices with in that. This
app itself does not handle the Computer Vision and unlocking of the physical door.
Instead, physical door interaction is handled by a different Python program; the
door program interacts with this API by making HTTP requests to a TCP/IP socket.
(Yes, it's not the best choice, UNIX sockets would be better. Can't you tell
the guy who did this is a Web guy?)

### Testing

To run the test suite, one can consult the documentation on pytest to
launch the test quite. Alternatively, one can also do 
```(sudo) docker build --tag=door-unlock-api:latest --target=test .``` and then
```docker run door-unlock-api:latest```Visual Studio Code with the Python extension
 also helpfully lets you run the test suite.

If one is using a debugger, please note for each test module is intended to run at once. As of this
time, each test case is interdependent of each other and relies on the successful execution
of the previous test to work correctly. Specifically, this is due to use of module scoping for
the test fixtures. For more information, please refer to the pytest documentation on fixtures 
and fixture scoping.

### Deployment

For deployment in production, the intention is to use Docker and Docker Compose.
This hopefully will simplify deployment and integration with CI (this is the
primary reason that the application communicates over IP sockets. Sharing a SQLite
database between containers was uncertain, especially given that concurrent database
access for SQLite is dependent on file locks/synchronization primitives).

### Endpoints

This is still largely in progress. REST resources are being determined and 
tests are being created gradually. The test suite is not meant to be
comprehensive, just enough to verify very basic operations. The following is a
outline of the endpoints and methods available:

#### /users ####

* POST
    - Creates user
    - Note that certain fields need to match things in Slack workspace for interop.
    - Returns a 201 upon success
* PUT
    - same as POST, used as bulk udpate
    - Should expect idempotent operations

* DELETE
    - Removes users
    - Note this is protected route, user must be authenticate and contain the correct
    role and permissions to do so.

#### /users/sso ###
 
* Not implemented yet, will be used to support single sign on when web application
  gets going
* This is largely out of scope for this document but hypothetically speaking, this
  base endpoint would be used to forward authorization tokens and verified
  (if supported)

#### /user ####

* POST
    - logs/authenticates the user for web portal
    - returns a cookie with a JWT to act as authentication credentials

#### /users/{username}/profile ####
*Note this is a protected route, JWT subject and username must match*

* POST
    - Updates profiles

* GET
    - retrieves profile information for a given ```username```

#### /slackbot ####

* TBD, will be the base path for all Slack bot interactions (need to work
  out authentication and hand off)
* Restricted interactions here may leverage channel membership as authentication
  mechanism.


