style_css = """
/*https://www.materialui.co/flatuicolors*/

QMainWindow {
    background-color: #ecf0f1;
    border: 1px solid #000000;
}

/*QMenuBar {*/
/*	background-color: #323a3d;*/
/*    color: rgb(238, 238, 238);*/
/*}*/
/*QMenuBar, QStatusBar {*/
/*    background-color: #000000;*/
/*}*/

/*QMenuBar::item {*/
/*    !*spacing: 3px;*!*/
/*    !*padding: 6px;*!*/
/*    background: transparent;*/
/*    border-right: 1px solid #ffffff;*/
/*}*/

/*QMenuBar::item:selected {*/
/*    background: #ffffff;*/
/*}*/

/*QMenuBar::item:pressed {*/
/*    background: #f1fff1;*/
/*}*/

/*QMenu {*/
/*    background-color: white;*/
/*    margin: 2px; !* some spacing around the menu *!*/
/*}*/

/*QMenu::item {*/
/*    padding: 2px 25px 2px 20px;*/
/*    border: 1px solid transparent; !* reserve space for selection border *!*/
/*}*/

/*QMenu::item:selected {*/
/*    border-color: rgb(112, 112, 138);*/
/*    background: rgba(100, 100, 100, 150);*/
/*}*/

QWidget {
    background-color: #f6f6f6;
    color: #000000;
    /* font: 75 10pt "Yu Gothic UI Light"; */
    /*font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;*/
    font: 10pt;
    /* border: 0px; */
    border: 1px;
}

/*
#nodeView {
    border: 0px;
    outline: none;
}

#nodeScene {
    border: 0px;
    outline: none;
} */

/*QGraphicsProxyWidget {*/
/*    background-color: transparent;*/
/*}*/

/*QToolButton#proxyWidgetTollButton {*/
/*    font: 14px;*/
/*    background-color: transparent;*/
/*    padding: 0px;*/
/*    color: rgb(255, 255, 255);*/
/*    border: 1px solid rgb(250, 209, 29);*/
/*    border-radius: 10px;*/
/*}*/

/*QToolButton#proxyWidgetTollButton:hover {*/
/*    background-color: rgb(236, 37, 22);*/
/*}*/

/*QToolButton#proxyWidgetTollButton:pressed {*/
/*    background-color: rgb(236, 221, 10);*/
/*}*/


/*QSplitter::handle {*/
/*    background-color: #bfc1c9;*/
/*    border: 0px;*/
/*    outline: none;*/
/*}*/

/*QSplitter::handle:hover {*/
/*    background-color: #001aff;*/
/*}*/

/*QLabel#proxyWidgetLabel {*/
/*    background-color: rgba(0, 0, 0, 0);*/
/*    color: rgb(255, 255, 255);*/
/*    font: 75 11pt "Yu Gothic UI";*/
/*}*/


/*QLabel#label_Panal_2, #label_Panal {*/
/*    background-color: #676d7c;*/
/*    color: rgb(30, 30, 31);*/
/*    padding: 4px;*/
/*    font: 75 12pt "Yu Gothic UI";*/
/*}*/

/*QLabel#label_nodeType {*/
/*    background-color: #995228;*/
/*    color: rgb(252, 250, 228);*/
/*    padding: 2px;*/
/*    border-radius: 10px;*/
/*}*/

/*QLabel#label_nodeVersion {*/
/*    background-color: #919928;*/
/*    color: rgb(252, 250, 228);*/
/*    padding: 2px;*/
/*    border-radius: 8px;*/
/*}*/

QGroupBox {
    background-color: #dcdcdc;
    /*padding: 0px;*/
    border: 1px solid #d2d1d2;
    border-radius: 5px;
}

QPushButton {
    background-color: #ffffff;
    Text-align:center;
    /*font: 11px;*/
    /*font-weight: bold;*/
    color: #000000;
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

QComboBox {
    background-color: #ffffff;
    Text-align:center;
    /*font: 11px;*/
    /*font-weight: bold;*/
    color: #000000;
    padding: 0px;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
}
QComboBox:hover {
    border: 1.5px solid #106bfd;
    color: #ffffff;
}
QComboBox:focus {
    border: 1.5px solid #56aafb;
}

/*QToolButton {*/
/*    background-color: rgb(155, 113, 49);*/
/*    font: 12px;*/
/*    padding: 4px;*/
/*    color: rgb(255, 255, 255);*/
/*    border: 1px solid rgb(202, 202, 202);*/
/*    !* border: 1px solid rgb(157, 151, 255); *!*/
/*}*/
/*QToolButton:hover {*/
/*    background-color: rgb(204, 151, 71);*/
/*}*/
/*QToolButton:pressed {*/
/*    background-color: rgb(110, 79, 33);*/
/*}*/

/*QToolButton:disabled {*/
/*    background-color: rgb(109, 109, 109);*/
/*    color: rgb(173, 173, 173);*/
/*}*/

QLabel {
    background-color: rgba(255, 255, 241, 0);
    /*font: 11px;*/
}

QCheckBox {
    background-color: rgba(255, 255, 241, 0);
    /*font: 11px;*/
}

QRadioButton{
    background-color: rgba(255, 255, 241, 0);
    /*font: 11px;*/
}

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

QSlider {
    background-color: rgba(255, 255, 241, 0);
    /*font: 11px;*/
}

QTableView {
    background-color: #ffffff;
}

QDoubleSpinBox {
    background-color: #ffffff;
    border: 1px solid #d2d1d2;
    border-radius: 5px;
    padding-right: 15px; /* make room for the arrows */
    /*border-width: 5px;*/
    color: #000000;
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
/*QDoubleSpinBox::up-button {*/
/*    color: black;*/
/*    background-color: #2f0099;*/
/*    !*subcontrol-origin: border;*!*/
/*    !*subcontrol-position: top right; !* position at the top right corner *!*!*/
/*    padding-right: 2px;*/
/*    width: 16px; !* 16 + 2*1px border-width = 15px padding + 3px parent border *!*/
/*    border-width: 1px;*/
/*}*/

/*QSpinBox::up-button:hover {*/
/*    border-image: url(:/images/spinup_hover.png) 1;*/
/*}*/

/*QSpinBox::up-button:pressed {*/
/*    border-image: url(:/images/spinup_pressed.png) 1;*/
/*}*/

/*QSpinBox::up-arrow {*/
/*    image: url(:/images/up_arrow.png);*/
/*    width: 7px;*/
/*    height: 7px;*/
/*}*/

/*QSpinBox::up-arrow:disabled, QSpinBox::up-arrow:off { !* off state when value is max *!*/
/*   image: url(:/images/up_arrow_disabled.png);*/
/*}*/

/*QSpinBox::down-button {*/
/*    subcontrol-origin: border;*/
/*    subcontrol-position: bottom right; !* position at bottom right corner *!*/

/*    width: 16px;*/
/*    border-image: url(:/images/spindown.png) 1;*/
/*    border-width: 1px;*/
/*    border-top-width: 0;*/
/*}*/

/*QSpinBox::down-button:hover {*/
/*    border-image: url(:/images/spindown_hover.png) 1;*/
/*}*/

/*QSpinBox::down-button:pressed {*/
/*    border-image: url(:/images/spindown_pressed.png) 1;*/
/*}*/

/*QSpinBox::down-arrow {*/
/*    image: url(:/images/down_arrow.png);*/
/*    width: 7px;*/
/*    height: 7px;*/
/*}*/

/*QSpinBox::down-arrow:disabled,*/
/*QSpinBox::down-arrow:off { !* off state when value in min *!*/
/*   image: url(:/images/down_arrow_disabled.png);*/
/*}*/

/*QTreeView, QListView {*/
/*    border: 0px;*/
/*    outline: none;*/
/*    background-color: #222525;*/
/*}*/

/*QTreeView::item, QListView::item  {*/
/*	border: 0px;*/
/*    outline: none;*/
/*    background-color: #222525;*/
/*}*/

/*QTreeView::branch {*/
/*    background-color: #222525;*/
/*}*/

/*QTreeView::item:hover, QListView::item:hover {*/
/*    background-color: #434b4e;*/
/*    border-top: 1px solid #a8a8a8;*/
/*    border-bottom: 1px solid #a8a8a8;*/
/*}*/

/*QTreeView::item:selected, QListView::item:hover {*/
/*    background-color: #4e4d53;*/
/*    border-top: 1px solid #a8a8a8;*/
/*    border-bottom: 1px solid #a8a8a8;*/
/*}*/

/*QTreeView::branch:has-siblings:!adjoins-item {*/
/*    border-image: url("resource/images/vline.png") 0;*/
/*}*/

/*QTreeView::branch:has-siblings:adjoins-item {*/
/*    border-image: url("resource/images/branch-more.png") 0;*/
/*}*/

/*QTreeView::branch:!has-children:!has-siblings:adjoins-item {*/
/*    border-image: url("resource/images/branch-end.png") 0;*/
/*}*/

/*QTreeView::branch:has-children:!has-siblings:closed,*/
/*QTreeView::branch:closed:has-children:has-siblings {*/
/*        border-image: none;*/
/*        image: url("resource/images/branch-closed.png");*/
/*}*/

/*QTreeView::branch:open:has-children:!has-siblings,*/
/*QTreeView::branch:open:has-children:has-siblings  {*/
/*        border-image: none;*/
/*        image: url("resource/images/branch-open.png");*/
/*}*/

QHeaderView::section {
    background-color: rgb(210, 209, 210);
    color: rgb(15, 15, 15);
    border: 0px;
    border-right: 1px solid  rgb(15, 15, 15);
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    outline: none;
}

/* QFrame {
    border: 1px solid rgb(255, 0, 0);
} */

/*QTabBar::tab {*/
/*    border: 1px solid #C4C4C3;*/
/*    border-bottom-color: #C2C7CB;*/
/*    border-top-left-radius: 4px;*/
/*    border-top-right-radius: 4px;*/
/*    min-width: 8ex;*/
/*    padding: 2px;*/
/*    margin-right: 2px;*/
/*}*/

/*QTabBar::tab:selected {*/
/*    background-color: rgb(173, 159, 100);*/
/*    color: rgb(15, 15, 15);*/
/*}*/
/*QTabBar::tab:!selected {*/
/*    background-color: rgb(165, 165, 165);*/
/*    color: rgb(88, 88, 88);*/
/*    font: 10pt;*/
/*}*/

/*
SCROLLBAR
*/

QScrollBar:vertical {
    width: 10px;
}

QScrollBar:horizontal {
	height: 10px;
}

QScrollBar:vertical,
QScrollBar:horizontal{
	margin: 0px;
	border: 0px solid grey;
	background: rgba(255, 255, 255, 0);
}

QScrollBar::handle:vertical,
QScrollBar::handle:horizontal{
	min-height: 0px;
    background: #56aafb;
    /*border-radius: 5px;*/
}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:horizontal:hover {
	background: #106bfd;
}

/*QScrollBar::add-line:vertical,*/
/*QScrollBar::add-line:horizontal {*/
/*	height: 0px;*/
/*	border: 0px solid grey;*/
/*	subcontrol-origin: margin;*/
/*	subcontrol-position: bottom;*/
/*	background: rgb(80, 80, 80);*/
/*}*/

/*QScrollBar::sub-line:vertical,*/
/*QScrollBar::sub-line:horizontal {*/
/*	height: 0px;*/
/*	border: 0px solid grey;*/
/*	subcontrol-position: top;*/
/*	subcontrol-origin: margin;*/
/*	background: rgb(80, 80, 80);*/
/*}*/

/*QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {*/
/*	width: 0px;*/
/*	height: 0px;*/
/*	border: 0px;*/
/*	background: white;*/
/*}*/

/*QScrollBar::add-page:horizontal, QScrollBar::add-page:vertical,*/
/*QScrollBar::add-page:horizontal, QScrollBar::sub-page:vertical {*/
/*	background: none;*/
/*}*/

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
"""

def style():
    return style_css