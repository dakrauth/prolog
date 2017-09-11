#!/usr/bin/env python3
import os
import io
import sys
import logging
import logging.config
from pprint import pprint
import prolog
from prolog.config import config, config_dict

try:
    import ipdb as pdb
except ImportError:
    import pdb


try:
    import logging_tree
except ImportError:
    logging_tree = None


def reset_logging():
    logging._acquireLock()
    try:
        logging.root.manager.loggerDict.clear()
        prolog.reset_handlers()
    finally:
        logging._releaseLock()


class register:
    def __init__(self):
        self._items = {}
        self.reset = True
    def __call__(self, func):
        self._items[func.__name__] = func
    def names(self):
        return list(self._items.keys())
    def execute(self, name, _pdb=False):
        print('{sep}\nExecuting {name}\n{sep}'.format(name=name, sep='-' * 20))
        func = self._items[name]
        if _pdb:
            pdb.set_trace()
        if self.reset:
            reset_logging()
        func()
        print()
register = register()


def log_all_levels(logger):
    logger.error('This is an error log message')
    logger.warning('This is an warn log message')
    logger.info('This is an info log message')
    logger.debug('This is an debug log message')
    if logging_tree:
        print('\nLogging Tree:')
        logging_tree.printout()



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


@register
def simple():
    prolog.basic_config('simple', 'DEBUG', handlers='stream')
    logger = logging.getLogger('simple')
    log_all_levels(logger)


@register
def stream():
    iostr = io.StringIO()
    stream_hdlr = prolog.stream_handler(level='DEBUG',formatter='short', stream=iostr)
    prolog.basic_config('stream', 'DEBUG', stream_hdlr)
    logger = logging.getLogger('stream')
    log_all_levels(logger)
    print('iostream value:')
    print(iostr.getvalue())


@register
def dictconfig():
    cfg = config_dict()
    dct = config_dict('dictconfig', 'DEBUG')
    logging.config.dictConfig(dct)
    logger = logging.getLogger('dictconfig')
    log_all_levels(logger)


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
