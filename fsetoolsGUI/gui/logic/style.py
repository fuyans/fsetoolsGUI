style_css = """

/*https://www.materialui.co/flatuicolors*/

/* =================================================== QLabel ======================================================= */

QMainWindow {
    background-color: #ecf0f1;
    border: 1px solid #000000;
}

/* =================================================== QLabel ======================================================= */

QWidget {
    background-color: #f6f6f6;
    color: #000000;
    /* font: 75 10pt "Yu Gothic UI Light"; */
    /*font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;*/
    /*font: 10pt;*/
    /* border: 0px; */
    border: 1px;
}

/* =================================================== QLabel ======================================================= */

QGroupBox {
    background-color: #dcdcdc;
    /*padding: 0px;*/
    border: 1px solid #d2d1d2;
    border-radius: 5px;
}

/* =================================================== QLabel ======================================================= */

QLabel {
    background-color: rgba(255, 255, 241, 0);
}
QLabel {
    background-color: rgba(255, 255, 241, 0);
}

/* ================================================= QPushButton ==================================================== */

QPushButton {
    background-color: #ffffff;
    Text-align:center;
    /*color: #000000;*/
    padding: 0px;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
}
QPushButton:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
    color: #ffffff;
    border: 0px;
}
QPushButton:focus {
    border: 1.5px solid #56aafb;
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

/* ================================================== QLineEdit ===================================================== */

QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
    /* color: rgb(235, 242, 250); */
}
QLineEdit:hover {
    background-color: #ffffff;
    border: 1.5px solid #56aafb;
    border-radius: 5px;
    /* color: rgb(235, 242, 250); */
}
QLineEdit:focus {
    background-color: #ffffff;
    border: 1.5px solid #106bfd;
    border-radius: 5px;
    /* color: rgb(235, 242, 250); */
}
QLineEdit:disabled {
    background-color: #bdc3c7;
    border: 1px solid #bdc3c7;
    color: rgb(187, 187, 187);
}

/* ================================================== QCheckBox ===================================================== */

QCheckBox {
    background-color: rgba(255, 255, 241, 0);
}

/* ================================================== QComboBox ===================================================== */

QComboBox
{
    background-color: white;
    color: black;
    selection-background-color: #56aafb;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
    padding: 0.5px;
}
QComboBox:hover
{
    background-color: #ffffff;
    border: 1.5px solid #56aafb;
    padding: 0px;
}
QComboBox:focus, QComboBox:on
{
    background-color: #ffffff;
    border: 1.5px solid #106bfd;
    padding: 0px;
}
QComboBox::drop-down
{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    border-radius: 5px;
    border-left-width: 0px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}
QComboBox::down-arrow
{
    image: url(gui/images/down.png);
    margin-right: 10px;
    padding: 1.5px;
}
QComboBox::down-arrow:hover
{
    image: url(gui/images/down-sky.png);
    margin-right: 10px;
    padding: 0px;
}
QComboBox::down-arrow:on, QComboBox::down-arrow:focus
{
    image: url(gui/images/down-ocean.png);
    margin-right: 10px;
}
/*QComboBox::down-arrow:on, QComboBox::down-arrow:hover,*/
/*QComboBox::down-arrow:focus*/
/*{*/
/*    image: url(:/qss_icons/rc/down_arrow.png);*/
/*}*/

/* ================================================ QDoubleSpinBox ================================================== */
/*https://stackoverflow.com/questions/9389770/qspinbox-arrows-place-outside-line-edit-css*/

QDoubleSpinBox {
    background-color: white;
    color: black;
    selection-background-color: #56aafb;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
    padding-right: 15px; /* make room for the arrows */
}
QDoubleSpinBox:hover {
    background-color: #ffffff;
    border: 1.5px solid #56aafb;
    border-radius: 5px;
}
QDoubleSpinBox:focus {
    background-color: #ffffff;
    border: 1.5px solid #106bfd;
    border-radius: 5px;
}
QDoubleSpinBox::down-arrow
{
    image: url(gui/images/down.png);
    margin-right: 10px;
}

/* ================================================= QRadioButton =================================================== */

QRadioButton{
    background-color: rgba(255, 255, 241, 0);
    /*font: 11px;*/
}

/* ================================================== QTableView ==================================================== */

QTableView {
    background-color: #ffffff;
}

/* ================================================== QScrollBar ==================================================== */

QScrollBar:vertical {
    border: 0px solid #999999;
    background: rgba(0, 0, 0, 0);
    width:12px;
    margin: 1px 1px 1px 1px;
}
QScrollBar::handle:vertical {
    min-height: 50px;
    border-radius: 5px;
    background-color: #d2d1d2;
}
QScrollBar::handle:vertical:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
}
QScrollBar::handle:vertical:pressed {
    background-color: #106bfd;
}
QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

/* ================================================= QProgressBar =================================================== */

QProgressBar {
    border: 1px solid #d2d1d2;
    border-radius: 5px;
}
QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
    border-radius: 5px;
    /*width: 20px;*/
    /*margin: 0.5px;*/
}

/* =================================================== QSlider ====================================================== */

/* horizontal */

QSlider:horizontal {
    border: 0px solid #d2d1d2;
    background: rgba(0, 0, 0, 0);
    height: 2px;
}
QSlider::groove:horizontal {
    border: 0px solid #d2d1d2;
    background: #d2d1d2;
    height: 2px;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: white;
    border-radius: 4px;
}
QSlider::add-page:horizontal {
    background: #d2d1d2;
    border: 0px solid #d2d1d2;
    height: 10px;
    border-radius: 4px;
}
QSlider::handle:horizontal {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #56aafb, stop: 0.4 #3295fd, stop:1 #106bfd);
    /*border: 1px solid #777;*/
    width: 10px;
    margin-top: -4px;
    margin-bottom: -4px;
    border-radius: 5px;
}
QSlider::handle:horizontal:hover {
    background-color: #106bfd;
}
QSlider::sub-page:horizontal:disabled {
    background: #bbb;
    border-color: #999;
}
QSlider::add-page:horizontal:disabled {
    background: #eee;
    border-color: #999;
}
QSlider::handle:horizontal:disabled {
    background: #eee;
    border: 1px solid #aaa;
    border-radius: 4px;
}
"""

def style():
    return style_css