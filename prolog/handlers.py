import logging
import logging.handlers
from .utils import DEFAULT_LEVEL
from . import formatters

__all__ = ['create_handler', 'stream_handler', 'file_handler', 'get_handlers']


def create_handler(handler_cls, level=DEFAULT_LEVEL, formatter=None, **kwargs):
    formatter = formatters.get_formatter(formatter)
    h = handler_cls(**kwargs)
    h.setFormatter(formatter)
    h.setLevel(level)
    return h


def stream_handler(level=DEFAULT_LEVEL, formatter='color'):
    return create_handler(logging.StreamHandler, level, formatter)


def file_handler(
    level=DEFAULT_LEVEL,
    formatter='long',
    filename='prolog.log',
    maxBytes=0,
    backupCount=0
):
    return create_handler(
        logging.handlers.RotatingFileHandler,
        level,
        formatter,
        filename=filename,
        maxBytes=maxBytes,
        backupCount=backupCount
    )


registered_handlers = {
    'stream': stream_handler,
    'file': file_handler
}


def get_handlers(names, level):
    handlers = []
    for name in names.split(','):
        try:
            handler = registered_handlers[name]
        except KeyError:
            raise NameError(
                '"{}" is not a recognized handler shortcut'.format(name)
            )

        if not isinstance(handler, logging.Handler):
            handler = handler(level)
            registered_handlers[name] = handler
        
        handlers.append(handler)

    return handlers
