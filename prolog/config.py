import os
import json

CONFIG_DIRNAME = os.path.join(os.environ.get(
    'XDG_CONFIG_HOME',
    os.path.join(os.path.expanduser('~'), '.config')
), 'pyprolog')

CONSTANTS = {'TRUE': True, 'FALSE': False, 'NONE': None}

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

    STREAM_LEVEL = LEVEL
    STREAM_FORMATTER = 'color'
    STREAM_STREAM = 'sys.stderr'

    FILE_LEVEL = LEVEL
    FILE_FORMATTER = 'long'
    FILE_FILENAME = 'pypro.log'
    FILE_MAX_BYTES = 0
    FILE_BACKUP_COUNT = 0

    def __init__(self, env_prefix='PYPROLOG_'):
        self.env_prefix = env_prefix
        self.load_cfg()
        self.load_env()

    @property
    def config_filename(self):
        if '__config_filename' not in self.__dict__:
            cfg_filename = os.environ.get('{}_CONFIG'.format(self.env_prefix), None)
            if not cfg_filename:
                cfg_filename = os.path.join(CONFIG_DIRNAME, 'config.json')
            self.__config_filename = cfg_filename
        return self.__config_filename

    def load_cfg(self):
        if os.path.exists(self.config_filename):
            with open(self.config_filename) as fp:
                data = json.load(fp)

            self.update(**data)

    @property
    def data(self):
        return {k: getattr(self, k) for k in dir(self) if k.isupper()}

    def save_cfg(self):
        dirname = os.path.dirname(self.config_filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(self.config_filename, 'w') as fp:
            json.dump(self.data, fp, indent='    ')

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
