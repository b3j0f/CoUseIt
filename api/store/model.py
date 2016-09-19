from ..db import db
from ..rest import create_api


@create_api
class Store(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner = db.relationship(
        'User', backref=db.backref('stores', lazy='dynamic'), lazy='dynamic'
    )

