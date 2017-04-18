from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    category = db.Column(db.String(255))
    url = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.Date, default=datetime.datetime.now())
    updated_at = db.Column(db.Date, onupdate=datetime.datetime.now())

    def __init__(self, name, author, category, url, description):
        self.name = name
        self. author = author
        self.category = category
        self.url = url
        self.description = description

    def __repr__(self):
        return "Book %r" % self.name