from flask import Flask, Response, jsonify, url_for
from flask_restful import Resource, Api

app = Flask(__DoorUnlockAPI__)
api = Api(app)


@app.route('/')
def hello():
    return jsonify('Hello from Door Unlocker API')

if __name__ == '__main__':
    app.run()
