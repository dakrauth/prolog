#!/usr/bin/env python3
import os
import io
import sys
import logging
from pprint import pprint
import prolog
from prolog.config import config

try:
    import ipdb as pdb
except ImportError:
    import pdb


class register:
    def __init__(self):
        self._items = {}
    def __call__(self, func):
        self._items[func.__name__] = func
    def names(self):
        return list(self._items.keys())
    def execute(self, name, _pdb=False):
        print('{sep}\nExecuting {name}\n{sep}'.format(name=name, sep='-' * 20))
        func = self._items[name]
        if _pdb:
            pdb.set_trace()
        func()
        print()
register = register()


@register
def printcfg():
    for key in dir(config):
        if key.isupper():
            print('{}: {}'.format(key, getattr(config, key)))


@register
def parsecolors():
    for test in [
        'DEBUG:red',
        'INFO:blue,green;WARN:black',
        'ERROR:,red;'
    ]:
        print(prolog.ColorFormatter.normalize_colors(test))

    plc = os.environ.get('PYPROLOG_LEVEL_COLORS')
    if plc:
        print('From env:', prolog.ColorFormatter.normalize_colors(plc))


def log_all_levels(logger):
    logger.error('This is error')
    logger.warning('This is warn')
    logger.info('This is info')
    logger.debug('This is debug')


@register
def simple():
    prolog.init('sample', 'DEBUG', handlers='stream')
    logger = logging.getLogger('sample')
    log_all_levels(logger)


@register
def stream():
    iostr = io.StringIO()
    stream_hdlr = prolog.stream_handler(level='DEBUG',formatter='short', stream=iostr)
    prolog.init('stream', 'DEBUG', stream_hdlr)
    logger = logging.getLogger('stream')
    log_all_levels(logger)
    print('iostream value:')
    print(iostr.getvalue())


def main():
    args = sys.argv[1:] or register.names()
    _pdb = False
    for arg in args:
        if arg == '--pdb':
            _pdb = True
            continue

        register.execute(arg, _pdb)
        _pdb = False


if __name__ == '__main__':
    if '--help' in sys.argv[1:]:
        print('Options:', list(register.names()))
    else:
        main()
