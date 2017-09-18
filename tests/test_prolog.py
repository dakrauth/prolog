def parsecolors():
    for test in [
        'DEBUG:red',
        'INFO:blue,green;WARN:black',
        'ERROR:,red;'
    ]:
        print(prolog.ColorFormatter.normalize_colors(test))

    plc = os.environ.get('PYPROLOG_LEVEL_COLORS')
    if plc:
        print('From env:', prolog.ColorFormatter.normalize_colors(plc))
