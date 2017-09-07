import logging
from .formatters import *
from .handlers import *

VERSION = (0, 1, 0)

def get_version():
    return '.'.join(map(str, VERSION))


def init(
    loggers=None,
    level='INFO',
    handlers=None,
    propagate=False,
    disable_existing=True
):
    logging._handlers.clear()
    del logging._handlerList[:]

    handlers = handlers or 'stream,file'
    if isinstance(handlers, str):
        handlers = get_handlers(handlers, level)

    if not loggers:
        loggers = [logging.root]
    elif isinstance(loggers, str):
        loggers = [logging.getLogger(name) for name in loggers.split(',')]

    for logger in loggers:
        logger.setLevel(level)
        logger.propagate = propagate
        for h in handlers:
            logger.addHandler(h)



