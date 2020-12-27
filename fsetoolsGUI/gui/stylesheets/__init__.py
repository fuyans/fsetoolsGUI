from os import path
from sys import platform

from fsetoolsGUI import __root_dir__
from fsetoolsGUI import logger

css_md = '''
table{
    border:3px solid #000;
    width:100%;
    text-align:left;
    border-collapse:collapse
}
table td, table th{
    border:1px solid #000;
    padding:5px 4px
}
table thead{
    border-bottom:3px solid black
}
table thead th{
    font-weight:400;
    text-align:left
}
table tfoot td{
    font-size:14px
}
'''

css_main_btn = '''
QPushButton {
    Text-align: left; 
    padding-left: 4px; 
    padding-right: 4px; 
    padding-top: 1px; 
    padding-bottom: 1px;
}
'''

css_app_btn = '''
QPushButton {
    padding-left:10px; 
    padding-right:10px; 
    padding-top:2px; 
    padding-bottom:2px;
}
'''

try:
    with open(path.join(__root_dir__, 'gui', 'stylesheets', 'flat.css'), 'r') as f:
        css_template_flat = f.read()
except FileNotFoundError:
    css_template_flat = None
    logger.error('UI stylesheet css_template_flat not found')

if platform == "linux" or platform == "linux2":
    # linux
    css_main_btn = None
    css_template_flat = None
    css_app_btn = None
elif platform == "darwin":
    # OS X
    css_main_btn = None
    css_template_flat = None
    css_app_btn = None
elif platform == "win32":
    # Windows...
    pass
