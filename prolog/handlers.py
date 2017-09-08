import logging
import logging.handlers
from .config import config
from . import formatters

__all__ = ['create_handler', 'stream_handler', 'file_handler', 'get_handlers']


def create_handler(cls, level=config.LEVEL, formatter=None, **kwargs):
    formatter = formatters.get_formatter(formatter)
    h = cls(**kwargs)
    h.setFormatter(formatter)
    h.setLevel(level)
    return h


def stream_handler(level=config.LEVEL, formatter='color', stream=None):
    return create_handler(
        logging.StreamHandler,
        level,
        formatter,
        stream=stream
    )


def file_handler(
    level=config.LEVEL,
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


def reset_handlers():
    logging._handlers.clear()
    del logging._handlerList[:]


def extract_items(names):
    if isinstance(names, str):
        names = names.split(',')
    elif not isinstance(names, (list, tuple)):
        names = [names]

    for name in names:
        if isinstance(name, str):
            for subname in name.split(','):
                yield subname
        else:
            yield name


def get_handlers(names, level, reset=True):
    handlers = []
    if reset:
        reset_handlers()

    for item in extract_items(names):
        if isinstance(item, logging.Handler):
            handler = item
        elif isinstance(item, str):
            try:
                handler = registered_handlers[item]
            except KeyError:
                raise NameError(
                    '"{}" is not a recognized handler shortcut'.format(item)
                )

            if not isinstance(handler, logging.Handler):
                handler = handler(level)
                registered_handlers[item] = handler
        else:
            handler = item(level)

        handlers.append(handler)

    return handlers
