from os import path

from fsetoolsGUI import logger, __root_dir__

md_css = 'table{border:3px solid ' \
         '#000;width:100%;text-align:left;border-collapse:collapse}table td,' \
         'table th{border:1px solid #000;padding:5px 4px}table thead{' \
         'border-bottom:3px solid black}table thead th{' \
         'font-weight:400;text-align:left}table tfoot td{font-size:14px}'

try:
    # qt_css = open(path.join(__root_dir__, 'gui', 'style.css'), "r").read()
    qt_css = None  # disable fancy style
except FileNotFoundError:
    qt_css = None
    logger.error('UI style file not found')
