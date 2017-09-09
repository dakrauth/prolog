import logging
from .formatters import *
from .handlers import *
from .config import config

VERSION = (0, 1, 0)

def get_version():
    return '.'.join(map(str, VERSION))


def init(
    loggers=None,
    level=config.LEVEL,
    handlers=config.HANDLERS,
    propagate=config.PROPAGATE,
    disable_existing=config.DISABLE_EXISTING,
    reset_handlers=config.RESET_HANDLERS,
):
    logging._acquireLock()
    try:
        handlers = get_handlers(handlers, level, reset_handlers)

        if not loggers:
            loggers = [logging.root]
        elif isinstance(loggers, str):
            loggers = [logging.getLogger(name) for name in loggers.split(',')]

        for logger in loggers:
            logger.setLevel(level)
            logger.propagate = propagate
            for h in handlers:
                logger.addHandler(h)
    finally:
        logging._releaseLock()
