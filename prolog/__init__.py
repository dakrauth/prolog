import logging
from .formatters import *
from .handlers import *
from .config import *

__version__ = (0, 1, 0)
__version_string__ = '.'.join(map(str, __version__))


def basic_config(
    loggers=None,
    level=None,
    handlers=None,
    propagate=None,
    reset_handlers=None,
    cfg=None
):
    cfg = cfg or config
    level = cfg.resolve('LEVEL', level, 'INFO')
    logging._acquireLock()
    try:
        handlers = get_handlers(
            cfg.resolve('HANDLERS', handlers),
            level,
            cfg.resolve('RESET_HANDLERS', reset_handlers)
        )
        for name in config.logger_names(loggers):
            logger = logging.getLogger(name)
            logger.setLevel(level)
            logger.propagate = cfg.resolve('PROPAGATE', propagate)
            for h in handlers:
                logger.addHandler(h)
    finally:
        logging._releaseLock()
