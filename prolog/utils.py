import os
import sys

USE_DEFAULT = object()
DEFAULT_LEVEL = os.environ.get('PROLOG_LEVEL', 'INFO')

_colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')

class Colorize:
    fg = {_colors[x]: '3{}'.format(x) for x in range(8)}
    bg = {_colors[x]: '4{}'.format(x) for x in range(8)}
    reset = '\x1b[0m'

    @classmethod
    def style(cls, fmt, text='', ):
        fmt = fmt.split(',')
        if len(fmt) == 1:
            fmt.append('')

        fg, bg = fmt
        code_list = []
        if fg:
            code_list.append(cls.fg[fg])
        
        if bg:
            code_list.append(cls.bg[bg])

        if code_list:
            return '{}{}'.format(
                '\x1b[{}m'.format(';'.join(code_list)),
                text or ''
            )

        return text

    @staticmethod
    def supported(stream=sys.stderr):
        return hasattr(stream, 'isatty') and stream.isatty()

del _colors

def to_str(value):
    """
    Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, str):
        return value
    
    elif isinstance(value, bytes):
        return value.decode()

    return repr(value)

