import sys
import logging
from textwrap import indent
from .config import config

__all__ = ['PrologFormatter', 'ColorFormatter']


class PrologFormatter(logging.Formatter):
    DEFAULT_FMT = config.LONG_FMT
    DEFAULT_DATEFMT = config.DATE_FMT
    DEFAULT_STYLE = config.STYLE_FMT

    def __init__(self, **kwargs):
        super().__init__(
            fmt=kwargs.get('fmt', self.DEFAULT_FMT),
            datefmt=kwargs.get('datefmt', self.DEFAULT_DATEFMT),
            style=kwargs.get('style', self.DEFAULT_STYLE)
        )

    @staticmethod
    def to_str(value):
        '''
        Convert value a string. If value is already a str or None, returne it
        unchanged. If value is a byte, decode it as utf8. Otherwise, fall back
        to the value's repr.
        '''
        if value is None:
            return ''

        if isinstance(value, str):
            return value
        
        elif isinstance(value, bytes):
            return value.decode()

        return repr(value)

    def formatException(self, ei):
        return indent(super().formatException(ei), '... ')

    def formatMessage(self, record):
        try:
            record.message = self.to_str(record.getMessage())
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        return super().formatMessage(record)
        #return formatted.replace("\n", "\n    ")


_colors = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')

class Colorize:
    fg = {_colors[x]: '3{}'.format(x) for x in range(8)}
    bg = {_colors[x]: '4{}'.format(x) for x in range(8)}
    reset = '\x1b[0m'

    @classmethod
    def style(cls, fg='', bg=''):
        code_list = []
        if fg:
            code_list.append(cls.fg[fg])
        
        if bg:
            code_list.append(cls.bg[bg])

        return '\x1b[{}m'.format(';'.join(code_list)) if code_list else ''

    @staticmethod
    def supported(stream=sys.stderr):
        return hasattr(stream, 'isatty') and stream.isatty()

del _colors


class ColorFormatter(PrologFormatter):
    DEFAULT_FMT = config.COLOR_LONG_FMT
    DEFAULT_COLORS = config.LEVEL_COLORS

    def __init__(self, colors=None, **kwargs):
        super().__init__(**kwargs)
        if Colorize.supported():
            self.colors = self.normalize_colors(colors or self.DEFAULT_COLORS)
        else:
            self.colors = {}
            
    @staticmethod
    def normalize_colors(colors):
        if isinstance(colors, str):
            colors = dict(
                bits.split(':') for bits in colors.split(';') if bits
            )

        return {key: val.split(',') for key, val in colors.items()}

    def set_colors(self, record):
        if record.levelname in self.colors:
            record.color = Colorize.style(*self.colors[record.levelname])
            record.endcolor = Colorize.reset
        else:
            record.color = record.endcolor = ''

    def formatMessage(self, record):
        self.set_colors(record)
        return super().formatMessage(record)


registered_formatters = {
    'long': PrologFormatter(),
    'short': PrologFormatter(fmt=config.SHORT_FMT, datefmt=None),
    'color': ColorFormatter(),
}
registered_formatters['default'] = registered_formatters['long']


def get_formatter(arg=None):
    if arg is None:
        return registered_formatters['default']
    elif isinstance(arg, logging.Formatter):
        return arg
    elif isinstance(arg, str):
        try:
            return registered_formatters[arg]
        except KeyError as e:
            msg = '"{}" unrecognized formatter shortcut'.format(arg)
            raise KeyError(msg) from e
    elif isinstance(arg, dict):
        return PrologFormatter(**arg)
    else:
        return PrologFormatter(*arg)

