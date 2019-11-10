from flask import Flask, Response, jsonify, url_for
from src.extensions import db, ma, api
import os
import yaml


def create_app(config):
    app = Flask(__name__)
    # Database/SQLAlchemy Setup
    currentDir = os.getcwd()
    dbName = config['SQLITE_DB_NAME']
    dbURI = f'sqlite:////{currentDir}/database/data/{dbName}'
    if config['PYTHON_ENV'] == 'testing':
        dbURI = 'sqlite://'
    app.config['ENV'] = config['PYTHON_ENV']
    app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    return app


def hello():
    return jsonify('Hello from Door Unlocker API')


if __name__ == '__main__':
    # load config from yaml file
    with open('config.yaml', 'r') as configFile:
        config = yaml.safe_load(configFile)

    app = create_app(config)
    app.run()
