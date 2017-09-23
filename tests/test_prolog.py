import os
import io
import json
import logging
import logging.config
from prolog import *

HERE = os.path.dirname(os.path.abspath(__file__))

def levels():
    return sorted([
        (k,v) for k,v in logging._levelToName.items()
        if v != 'NOTSET'
    ])


def log_all_levels(logger):
    for level, name in levels():
        logger.log(level, 'A sample {} message'.format(name.lower()))


def test_parse_colors():
    assert ColorFormatter.normalize_colors('DEBUG:red') == {'DEBUG': ['red']}
    assert ColorFormatter.normalize_colors('INFO:blue,green;WARNING:black') == {
        'INFO': ['blue', 'green'],
        'WARNING': ['black']
    }

def test_color_stream(cfg):
    iostr = io.StringIO()
    fmt = ColorFormatter()
    fmt.colors = fmt.normalize_colors('*:red,green')
    stream_hdlr = stream_handler(level='CRITICAL', formatter=fmt, stream=iostr)
    basic_config('color', 'CRITICAL', handlers=[stream_hdlr], cfg=cfg)
    logger = logging.getLogger('color')
    log_all_levels(logger)
    results = iostr.getvalue()
    assert Colorize.fg['red'] in results
    assert Colorize.bg['green'] in results
    assert Colorize.reset in results
    assert 'color:CRITICAL' in results

def test_bytes_and_exc(cfg):
    iostr = io.StringIO()
    stream_hdlr = stream_handler(level='DEBUG', formatter='short', stream=iostr)
    #import pdb; pdb.set_trace()
    basic_config('bytes', handlers=[stream_hdlr])
    logger = logging.getLogger('bytes')
    try:
        1 / 0
    except:
        logger.error('Oöps!'.encode(), exc_info=1)

    results = iostr.getvalue()
    print(results)
    assert 'Oöps!' in results


def test_io_stream(cfg):
    iostr = io.StringIO()
    stream_hdlr = stream_handler(level='DEBUG', formatter='short', stream=iostr)
    basic_config('stream', 'DEBUG', handlers=[stream_hdlr], cfg=cfg)
    logger = logging.getLogger('stream')
    log_all_levels(logger)
    results = iostr.getvalue().splitlines()
    print(results)
    assert len(results) == 5
    for i, (val, name) in enumerate(levels()):
        assert name in results[i]
        assert name.lower() in results[i]


def test_file(cfg):
    filename = os.path.join(HERE, 'test_prolog_file.log')
    file_hdlr = file_handler(level='ERROR', formatter='short', filename=filename)
    basic_config('file', 'DEBUG', handlers=[file_hdlr], cfg=cfg)
    logger = logging.getLogger('file')
    log_all_levels(logger)
    assert os.path.exists(filename)
    os.remove(filename)


def test_get_handlers(cfg):
    handlers = get_handlers('file,stream', 'NOTSET')
    assert isinstance(handlers[0], PrologFileHandler)
    assert isinstance(handlers[1], PrologStreamHandler)


def test_cfg_files(cfg):
    filename = '.pyprologtestrc'
    cfg.save_local_cfg()
    assert cfg.local_cfg_filename == filename
    assert os.path.exists(filename)

    cfg.SHORT_FMT = 'foo bar baz'
    data = cfg.load(load_user=False, load_env=False)
    cfg.update(**data)
    assert cfg.SHORT_FMT == PrologConfig.SHORT_FMT
    
    os.remove(filename)
    assert not os.path.exists(filename)

    data = cfg.load_cfg(__file__)
    assert data == {}

    cfg.SHORT_FMT = 'foo bar baz'
    cfg.reset()
    assert cfg.SHORT_FMT == PrologConfig.SHORT_FMT


def test_dict_config(cfg):
    dct = dict_config(loggers='foo,bar', cfg=cfg)
    assert 'foo' in dct['loggers']
    assert 'bar' in dct['loggers']
    assert 'root' not in dct

    dct = dict_config(cfg=cfg)
    assert 'root' in dct


def test_string_import(cfg):
    AppDirs = cfg.string_import('appdirs.AppDirs')
    assert hasattr(AppDirs, 'site_config_dir')

    try:
        cfg.string_import('foobarbazspameggs')
    except ImportError:
        assert True
    else:
        assert False

    try:
        cfg.string_import('tempfile.TemporaryDirectoryXYZ')
    except ImportError:
        assert True
    else:
        assert False



