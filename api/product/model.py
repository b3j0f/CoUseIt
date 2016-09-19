from ..db import db
from ..rest import create_api


@create_api
class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(255))

    supplier = db.relationship(
        'User', backref=db.backref('products', lazy='dynamic'), lazy='dynamic'
    )

    store = db.relationship(
        'Store', backref=db.backref('products', lazy='dynamic'), lazy='dynamic'
    )
