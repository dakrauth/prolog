import os
import json

path = os.path

CONFIG_DIRNAME = os.path.join(os.environ.get(
    'XDG_CONFIG_HOME',
    path.join(path.expanduser('~'), '.config')
), 'pyprolog')

CONSTANTS = {'TRUE': True, 'FALSE': False, 'NONE': None}

def absolute_path(pth):
    return path.normpath(path.expandvars(path.expanduser(pth)))


def data_dict(obj):
    return {k: getattr(obj, k) for k in dir(obj) if k.isupper() and k[0] != '_'}


class Config:
    LEVEL = 'INFO'
    SHORT_FMT = "{levelname}:{name} {message}"
    LONG_FMT = '[{asctime} {name}:{levelname}:{module}:{lineno}] {message}'

    COLOR_LONG_FMT = '{color}[{asctime} {name}:{levelname}:{module}:{lineno}]{endcolor} {message}'
    COLOR_SHORT_FMT = '{color}{levelname}:{name}{endcolor} {message}'
    LEVEL_COLORS = 'DEBUG:magenta;INFO:blue;WARNING:white,yellow;ERROR:white,red'

    DATE_FMT = "%Y-%m-%dT%H:%M:%S"
    STYLE_FMT = '{'

    HANDLERS = 'stream,file'
    PROPAGATE = False
    DISABLE_EXISTING = True
    RESET_HANDLERS = True

    STREAM_LEVEL = 'NOTSET'
    STREAM_FORMATTER = 'color'
    STREAM_STREAM = 'sys.stderr'

    FILE_LEVEL = 'NOTSET'
    FILE_FORMATTER = 'long'
    FILE_FILENAME = 'pypro.log'
    FILE_MAX_BYTES = 0
    FILE_BACKUP_COUNT = 0

    def __init__(self, env_prefix='PYPROLOG_', local_cfg_filename='.pyprolog'):
        self.env_prefix = env_prefix
        self.local_cfg_filename = absolute_path(local_cfg_filename)
        
        fn = os.environ.get('{}_CONFIG'.format(self.env_prefix), None)
        self.user_cfg_filename = absolute_path(fn) if fn else path.join(
            CONFIG_DIRNAME,
            'config.json'
        )

        self.load()

    def load(self):
        self.load_cfg(self.user_cfg_filename)
        self.load_cfg(self.local_cfg_filename)
        self.load_env()

    def load_cfg(self, filename=None):
        fpath = absolute_path(filename) if filename else self.user_cfg_filename
        if path.exists(fpath):
            with open(fpath) as fp:
                data = json.load(fp)

            self.update(**data)

    def data(self):
        return data_dict(self)

    @classmethod
    def default_data(self):
        return data_dict(cls)

    def remove_cfg(self):
        if path.exists(self.user_cfg_filename):
            os.remove(self.user_cfg_filename)

    def save_cfg(self, filename=None):
        fpath = absolute_path(filename) if filename else self.user_cfg_filename
        dirname = path.dirname(fpath)
        if dirname and not path.exists(dirname):
            os.makedirs(dirname)

        with open(self.user_cfg_filename, 'w') as fp:
            json.dump(self.data(), fp, indent='    ')

    def load_env(self):
        n = len(self.env_prefix)
        for key, value in (
            (k[n:], v)
            for k,v in os.environ.items()
            if k.startswith(self.env_prefix)
        ):
            key = key.upper()
            if hasattr(self, key):
                value = CONSTANTS.get(value.upper(), value)
                setattr(self, key, value)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

    def logger_names(self, names=None):
        if not names:
            names = [None]
        elif isinstance(names, str):
            names = names.split(',')

        return names

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


def config_dict(
    loggers=None,
    level=config.LEVEL,
    propagate=config.PROPAGATE,
    disable_existing=config.DISABLE_EXISTING,
):
    dct = {
        'version': 1,
        'disable_existing_loggers': disable_existing,
        'formatters': {
            'long': {
                '()': 'prolog.formatters.PrologFormatter',
                'format': config.LONG_FMT,
                'datefmt': config.DATE_FMT,
                'style': config.STYLE_FMT
            },
            'short': {
                '()': 'prolog.formatters.PrologFormatter',
                'format': config.SHORT_FMT,
                'datefmt': '',
                'style': config.STYLE_FMT
            },
            'color': {
                '()': 'prolog.formatters.ColorFormatter',
                'format': config.COLOR_LONG_FMT,
                'datefmt': config.DATE_FMT,
                'style': config.STYLE_FMT,
                'colors': config.LEVEL_COLORS
            }
        },
        'handlers': {
            'stream': {
                'class': 'prolog.handlers.PrologStreamHandler',
                'level': config.STREAM_LEVEL,
                'formatter': 'color',
            },
            'file': {
                'class': 'prolog.handlers.PrologFileHandler',
                'level': config.FILE_LEVEL,
                'formatter': 'long',
                'filename': config.FILE_FILENAME,
                'maxBytes': config.FILE_MAX_BYTES,
                'backupCount': config.FILE_BACKUP_COUNT
            }
        },
        'loggers': {}
    }

    handlers = config.HANDLERS.split(',')
    for name in config.logger_names(loggers):
        cfg = {'handlers': handlers, 'level': level, 'propagate': propagate}
        if name:
            dct['loggers'][name] = cfg
        else:
            dct['root'] = cfg

    return dct


