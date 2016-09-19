from flask import Flask

from config import config


def get_app(name=__name__, config=config):

    result = Flask(name)

    result.config.from_object(config)

    return result
