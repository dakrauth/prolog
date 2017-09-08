import os

class Config:
    LEVEL = 'INFO'
    SHORT_FMT = "{levelname}:{name} {message}"
    LONG_FMT = '[{asctime} {name}:{levelname}:{module}:{lineno}] {message}'

    COLOR_LONG_FMT = '{color}[{asctime} {name}:{levelname}:{module}:{lineno}]{endcolor} {message}'
    COLOR_SHORT_FMT = '{color}{levelname}:{name}{endcolor} {message}'
    LEVEL_COLORS = 'DEBUG:magenta;INFO:blue;WARNING:white,yellow;ERROR:white,red'

    DATE_FMT = "%Y-%m-%dT%H:%M:%S"
    STYLE_FMT = '{'

    def __init__(self, env_prefix='PYPROLOG_'):
        n = len(env_prefix)
        for key, value in (
            (k[n:], v) for k,v in os.environ.items() if k.startswith(env_prefix)
        ):
            if hasattr(self, key):
                setattr(self, key, value)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def resolve(dotted_path):
        try:
            mod_path, attr = dotted_path.rsplit('.', 1)
        except ValueError:
            raise ImportError('{} not a dotted path string'.format(dotted_path))

        mod = __import__(mod_path)

        try:
            return getattr(mod, attr)
        except AttributeError:
            raise ImportError('Module "{}" has no "{}" attribute'.format(
                mod_path, attr
            ))



config = Config()
