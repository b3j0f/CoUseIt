from api import app
from api.db import db
from api.utils import import_modules

from flask import g

from config import config

from logging import getLogger


def main():

    import_modules('api')

    db.create_all()

    app.run()


if __name__ == '__main__':

    main()
