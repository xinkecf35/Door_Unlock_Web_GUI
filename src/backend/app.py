from flask import Flask, Response, jsonify, url_for
from flask_restful import Resource, Api

app = Flask(__DoorUnlockAPI__)


@app.route('/')
def hello():
    return jsonify('Hello from Door Unlocker API')
