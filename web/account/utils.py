"""Utilities module."""
from __future__ import unicode_literals

from inspect import isroutine


def getprop(obj, name):
    """Get property."""
    result = ''
    for prop in name.split('.'):
        obj = getattr(obj, prop)
        if isroutine(obj):
            obj = obj()
        result = str(obj)
    return result


def tostr(obj, *fields):
    """Get obj representation."""
    return '{0}: {1}'.format(
        type(obj).__name__,
        '|'.join(
            ['{0}={1}'.format(field, getprop(obj, field)) for field in fields]
        )
    )
