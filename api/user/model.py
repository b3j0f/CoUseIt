from ..db import db
from .. import app
from ..rest import create_api


@create_api
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)


@create_api
class ForbiddenEmail(db.Model, FixturesMixin):

    fixtures = ['forbiddenemails.yaml']

    email = db.Column(db.String(256), primary_key=True)
