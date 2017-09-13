import json
import argparse
from pprint import pprint

try:
    import ipdb as pdb
except ImportError:
    import pdb

from . import config


def show(level=None, format=None):
    if level == 'user':
        data = config.load_cfg()
    elif level == 'default':
        data = config.default_data()
    elif level == 'env':
        data = config.load_env()
    else:
        data = config.data()

    if format == 'plain':
        for key in sorted(data.keys()):
            print('{} = {!r}'.format(key, data[key]))
    elif format == 'python':
        pprint(data)
    else:
        print(json.dumps(data, indent='    '))


def parse_args(args=None):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='prolog')
    parser.add_argument('--pdb', action='store_true')

    subparsers = parser.add_subparsers()

    # create the parser for the "show" command
    show_parser = subparsers.add_parser('show', help='show help')
    show_parser.set_defaults(func=show)
    show_parser.add_argument(
        'level',
        nargs='?',
        choices='default user env current'.split(),
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
