from config import config

from flask import Flask

from os import walk
from os.path import join


def import_modules(root='.', exclude=config.EXCLUDE):
    """Import modules from input root, in excluding input exclusion modules and
    returns imported modules in error with related error.

    :param str root: starting path.
    :param list exclude: modules to exclude."""

    for root, _, files in walk(root):
        if root in exclude:
            continue

        if root.startswith('./') or root.startswith('../'):
            root = root[root.index('/'):]

        for file in files:

            if file.endswith('.py'):

                fullname = join(root, file)[: -3].replace('/', '.')

                try:
                    __import__(fullname)

                except (ImportError, ValueError) as exc:
                    #logger.error(exc)
                    print(exc)


def get_app(name=__name__, config=config):
    """Get an instance of Flask with input name and specific configuration.

    :param str name: flask application name. Default is module name.
    :param type config: flask configuration. Default is application
        configuration.
    :rtype: Flask"""

    result = Flask(name)

    result.config.from_object(config)

    return result
