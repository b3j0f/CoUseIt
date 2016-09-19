from ..db import db
from ..rest import create_api


category_product = db.Table(
    'product_category',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


@create_api
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    products = db.relationship(
        'Product', secondary=category_product, lazy='dynamic',
        backref=db.backref('categories', lazy='dynamic')
    )
