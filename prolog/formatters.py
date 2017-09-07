import logging
from textwrap import indent
from .utils import Colorize, USE_DEFAULT, to_str

__all__ = ['PrologFormatter', 'ColorFormatter']

class PrologFormatter(logging.Formatter):
    DEFAULT_FMT = '[{asctime} {name}:{levelname}:{module}:{lineno}] {message}'
    DEFAULT_DATEFMT = '%Y-%m-%dT%H:%M:%S'
    DEFAULT_STYLE = '{'

    def __init__(self, **kwargs):
        super().__init__(
            fmt=kwargs.get('fmt', self.DEFAULT_FMT),
            datefmt=kwargs.get('datefmt', self.DEFAULT_DATEFMT),
            style=kwargs.get('style', self.DEFAULT_STYLE)
        )

    def formatException(self, ei):
        return indent(super().formatException(ei), '... ')

    def formatMessage(self, record):
        try:
            record.message = to_str(record.getMessage())
        except Exception as e:
            record.message = "Bad message (%r): %r" % (e, record.__dict__)

        return super().formatMessage(record)
        #return formatted.replace("\n", "\n    ")


class ColorFormatter(PrologFormatter):
    DEFAULT_FMT = '{color}[{asctime} {name}:{levelname}:{module}:{lineno}]{endcolor} {message}'
    DEFAULT_COLORS = {
        logging.DEBUG: 'magenta',
        logging.INFO: 'blue',
        logging.WARNING: 'white,yellow',
        logging.ERROR: 'white,red',
    }

    def __init__(self, colors=USE_DEFAULT, **kwargs):
        super().__init__(**kwargs)
        if colors and Colorize.supported():
            self.colors = self.DEFAULT_COLORS if colors is USE_DEFAULT else colors

    def set_colors(self, record):
        if record.levelno in self.colors:
            record.color = Colorize.style(self.colors[record.levelno])
            record.endcolor = Colorize.reset
        else:
            record.color = record.endcolor = ''

    def formatMessage(self, record):
        self.set_colors(record)
        return super().formatMessage(record)


SHORT_FMT = "{levelname}:{name} {message}"
DATE_FMT = "%Y-%m-%dT%H:%M:%S"
STYLE_FMT = '{'

registered_formatters = {
    'long': PrologFormatter(),
    'short': PrologFormatter(fmt=SHORT_FMT, datefmt=None),
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
        except KeyError:
            raise NameError(
                '"{}" is not a recognized formatter shortcut'.format(arg)
            )
    elif isinstance(arg, dict):
        return PrologFormatter(**arg)
    else:
        return PrologFormatter(*arg)


def register_formatters(**kwargs):
    global register_formatters
    register_formatters.update(kwargs)

