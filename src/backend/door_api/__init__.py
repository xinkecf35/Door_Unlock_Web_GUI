import os
import sys
from base64 import encodebytes

import yaml
from flask import Flask
from sqlalchemy import inspect

from .database import Role
from .extensions import db, ma
from .JSONResponse import JSONResponse

defaultConfig = {
   'SQLITE_DB_NAME': 'door-db.sqlite',
   'JWT_SECRET': encodebytes(os.urandom(32)),
   'PYTHON_ENV': 'development'
   ''
}


def _initializeDatabase(db):
    tableNames = inspect(db.engine).get_table_names()
    isEmpty = tableNames == []
    if isEmpty:
        db.create_all()
        role1 = Role(
            name='member',
            canUnlock=1,
            canManage=0,
            canAccessHistory=0)
        role2 = Role(
            name='admin',
            canUnlock=1,
            canManage=1,
            canAccessHistory=1)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()


def _registerBlueprints(app):
    from .routes import userBP, usersBP
    app.register_blueprint(usersBP)
    app.register_blueprint(userBP)


def _registerErrorHandlers(app):
    from .decorators import handleException
    from .decorators import handleBadRequest
    from .decorators import handleForbiddenRequest

    app.register_error_handler(400, handleBadRequest)
    app.register_error_handler(403, handleForbiddenRequest)
    app.register_error_handler(422, handleBadRequest)
    app.register_error_handler(500, handleException)


def create_app(config=defaultConfig):
    class APIFLask(Flask):
        response_class = JSONResponse

    app = APIFLask(__name__)
    if type(config) is dict:
        # Database/SQLAlchemy Setup
        currentDir = os.getcwd()
        dbName = config['SQLITE_DB_NAME']
        dbURI = f'sqlite:////{currentDir}/data/{dbName}'
        if config['PYTHON_ENV'] == 'testing':
            dbURI = 'sqlite://'
            app.config['TESTING'] = True
        app.config['ENV'] = config['PYTHON_ENV']
        app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
        app.config['SECRET_KEY'] = config['JWT_SECRET']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    db.app = app
    ma.app = app
    _registerBlueprints(app)
    _registerErrorHandlers(app)
    _initializeDatabase(db)
    return app


if __name__ == '__main__':
    # load config from yaml file
    try:
        with open('config.yaml', 'r') as configFile:
            config = yaml.safe_load(configFile)
    except OSError:
        print('Missing config file for flask app')
        # exit with no such file
        sys.exit(-2)
    app = create_app(config)
    app.run()
