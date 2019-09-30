from flask import Flask, Response, jsonify, url_for
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import pytest

# Global app variables setup
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
ma = Marshmallow()

# DB Setup
dbURI = 'sqlite://'
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['DEBUG'] = True
app.config['TESTING'] = True


@pytest.fixture(scope='session')
def app():
    with app.test_client() as client:
        db.init_app(app)
        yield client
