#!/usr/bin/env python3
import io
import os
import json
import argparse
import logging
import logging.config
from pprint import pprint

try:
    import logging_tree
except ImportError:
    logging_tree = None

try:
    import ipdb as pdb
except ImportError:
    import pdb

from . import *


def reset_logging():
    logging._acquireLock()
    try:
        logging.root.manager.loggerDict.clear()
        reset_handlers()
    finally:
        logging._releaseLock()


def log_all_levels(logger):
    logger.critical('This is a critical log message')
    logger.error('This is an error log message')
    logger.warning('This is a warning log message')
    logger.info('This is an info log message')
    logger.debug('This is a debug log message')
    if logging_tree:
        print('\nLogging Tree:')
        logging_tree.printout()


def simple(level='INFO'):
    basic_config('simple', handlers='stream', level=level)
    logger = logging.getLogger('simple')
    log_all_levels(logger)


def stream(level='INFO'):
    iostr = io.StringIO()
    stream_hdlr = stream_handler(level=level, formatter='short', stream=iostr)
    basic_config('stream', 'DEBUG', stream_hdlr)
    logger = logging.getLogger('stream')
    log_all_levels(logger)
    print('iostream value:')
    print(iostr.getvalue())


def dictconfig(level='INFO'):
    cfg = dict_config()
    dct = dict_config('dictconfig', level=level)
    logging.config.dictConfig(dct)
    logger = logging.getLogger('dictconfig')
    log_all_levels(logger)


samples = {f.__name__: f for f in [simple, stream, dictconfig]}


def sample_cmd(name, level):
    samples[name](level)


def show_cmd(level=None, format=None):
    if level == 'user':
        data = config.load_user_cfg()
    elif level == 'default':
        data = config.default_data()
    elif level == 'env':
        data = config.load_env()
    else:
        data = config.data()

    if format == 'python' or level == 'dict':
        pprint(data, indent=4)
    elif format == 'plain':
        for key in sorted(data.keys()):
            print('{} = {!r}'.format(key, data[key]))
    else:
        print(json.dumps(data, indent='    '))


def save_cmd(where='user'):
    if where == 'user':
        config.save_user_cfg()
    elif where == 'local':
        config.save_local_cfg()


def info_cmd():
    ucf = config.user_cfg_filename
    print('User config location:', ucf)
    print('    file exists: {}, directory exists: {}'.format(
        os.path.exists(ucf),
        os.path.exists(os.path.dirname(ucf))
    ))
    print('Local config filename:', config.local_cfg_filename)


def parse_args(args=None):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='prolog')
    parser.add_argument('--pdb', action='store_true')
    subparsers = parser.add_subparsers()

    info_parser = subparsers.add_parser('info', help='info help')
    info_parser.set_defaults(func=info_cmd)

    # create the parser for the "sample" command
    sample_parser = subparsers.add_parser('sample', help='sample help')
    sample_parser.set_defaults(func=sample_cmd)
    sample_parser.add_argument(
        'name',
        choices=list(samples.keys()),
        help='show some sample output'
    )
    sample_parser.add_argument(
        '--level',
        choices=list(logging._nameToLevel.keys()),
        default=config.LEVEL,
        help='set the logging level'
    )

    # create the parser for the "save" command
    save_parser = subparsers.add_parser('save', help='save help')
    save_parser.set_defaults(func=save_cmd)
    save_parser.add_argument(
        'location',
        choices='user local'.split(),
        help='save to either the user or local config file'
    )

    # create the parser for the "show" command
    show_parser = subparsers.add_parser('show', help='show help')
    show_parser.set_defaults(func=show_cmd)
    show_parser.add_argument(
        'level',
        nargs='?',
        choices='default user env dict current'.split(),
        default='current',
        help='show the config for a specific level'
    )
    show_parser.add_argument(
        '--format',
        choices='json python plain'.split(),
        default='json',
        help='format configuration as either json, python or plain text'
    )

    ns = parser.parse_args(args.split() if isinstance(args, str) else None)
    return vars(ns)

def main():
    args = parse_args()
    if args.pop('pdb', False):
        pdb.set_trace()

    func = args.pop('func', None)
    if func:
        func(**args)


if __name__ == '__main__':
    main()
