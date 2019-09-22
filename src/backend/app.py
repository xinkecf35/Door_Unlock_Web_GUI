from flask import Flask, Response, jsonify, url_for
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os
import yaml

# load config from yaml file
with open('config.yaml', 'r') as configFile:
    config = yaml.safe_load(configFile)

# Global app variables setup
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
ma = Marshmallow()

# Database/SQLAlchemy Setup
currentDir = os.getcwd()
dbName = config['SQLITE_DB_NAME']
dbURI = f'sqlite:////{currentDir}/database/data/{dbName}'
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI


def hello():
    return jsonify('Hello from Door Unlocker API')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run()
