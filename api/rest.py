from . import app
from .db import db
from flask_restless import APIManager

manager = APIManager(app, flask_sqlalchemy_db=db)


def create_api(*args, **kwargs):
    """Decorator for api creation from a model."""

    def _create_api(model):
        manager.create_api(model=model, *args, **kwargs)
        return model

    # used without arguments
    if len(args) == 1 and not kwargs and isinstance(args[0], db.Model):
        return _create_api(args[0])

    return _create_api
