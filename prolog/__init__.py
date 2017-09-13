import logging
from .formatters import *
from .handlers import *
from .config import config

__version__ = (0, 1, 0)
__version_string__ = '.'.join(map(str, __version__))


def basic_config(
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
        names = config.logger_names(loggers)

        for name in names:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.propagate = propagate
            for h in handlers:
                logger.addHandler(h)
    finally:
        logging._releaseLock()
