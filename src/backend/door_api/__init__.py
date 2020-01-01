import os
import yaml

from flask import Flask
from sqlalchemy import inspect

from .database import Role
from .extensions import db, ma


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
    from .routes import usersBP
    app.register_blueprint(usersBP)


def create_app(config):
    app = Flask(__name__)
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
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    db.app = app
    ma.app = app
    _registerBlueprints(app)
    _initializeDatabase(db)
    return app


if __name__ == '__main__':
    # load config from yaml file
    with open('config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)
    print(type(config))
    app = create_app(config)
    app.run()
