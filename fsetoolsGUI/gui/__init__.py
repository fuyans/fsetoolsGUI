from fsetoolsGUI import logger

md_css = 'table{border:3px solid ' \
         '#000;width:100%;text-align:left;border-collapse:collapse}table td,' \
         'table th{border:1px solid #000;padding:5px 4px}table thead{' \
         'border-bottom:3px solid black}table thead th{' \
         'font-weight:400;text-align:left}table tfoot td{font-size:14px}'

main_dialog_btn_css = '''
QPushButton {
    Text-align: center;
}
/*
QPushButton {
    background-color: #ffffff;
    Text-align: center;
    /*color: #000000;*/
    padding: 0px;
    padding-left: 1px;
    padding-right: 1px;
    padding-top: 2px;
    padding-bottom: 2px;
    border: 1px solid #d2d1d2;
    border-radius: 3px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
    color: #ffffff;
    border: 1.5px solid #56aafb;
}
QPushButton:focus {
    border: 1.5px solid #3295fd;
}
QPushButton:pressed {
    background-color: #106bfd;
}
QPushButton:disabled {
    background-color: #ecf0f1;
    /*font: 11px;*/
    padding: 3px;
    color: #98989d;
    border: 1px solid #d2d1d2;
}
*/
'''

try:
    qt_css = None  # disable fancy style
except FileNotFoundError:
    qt_css = None
    logger.error('UI style file not found')
