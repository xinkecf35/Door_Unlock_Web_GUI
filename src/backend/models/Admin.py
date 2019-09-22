from flask_sqlalchemy import SQLAlchemy
import config
import sqlite3


class Admin(Schema):

    def __init__(self, username):
        self.username = username
