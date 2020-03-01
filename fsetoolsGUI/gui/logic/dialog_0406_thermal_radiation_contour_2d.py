import sys

import matplotlib.pyplot as plt
from PySide2 import QtWidgets, QtGui

from fsetoolsGUI.gui.layout.dialog_0406_thermal_radiation_contour_2d import Ui_MainWindow
from fsetoolsGUI.gui.logic.OFRCustom import QMainWindow
from fsetools.lib.fse_thermal_radiation_2d_v2 import main, main_plot

from fsetoolsGUI.gui.logic.dialog_0002_tableview import TableModel, TableWindow

try:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )
except ModuleNotFoundError:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )


class Dialog0406(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(title='Thermal Radiation Analysis 2D', parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()

        # instantiate plot objects
        self.figure = plt.figure()
        self.figure.patch.set_facecolor('None')

        self.ax = self.figure.subplots()
        # self.figure, self.ax = plt.subplots()
        self.figure_canvas = FigureCanvas(self.figure)
        self.figure_canvas.setStyleSheet("background-color:transparent;")
        self.ui.verticalLayout_plot.addWidget(self.figure_canvas)
        # self.addToolBar(NavigationToolbar(self.figure_canvas, self))

        # instantiate variables
        self.param_dict = None  # input and output parameters

        # instantiate tables
        self.init_table()

        # signals
        self.ui.pushButton_submit.clicked.connect(self.submit)
        self.ui.pushButton_refresh.clicked.connect(self.update_plot)
        self.ui.pushButton_save_figure.clicked.connect(self.save_figure)
        self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_emitter_list_append.clicked.connect(self.table_emitters_insert)
        self.ui.pushButton_emitter_list_remove.clicked.connect(self.table_emitters_remove)

        # containers
        self.__is_first_submit: bool = True
        self.__solver_parameters: dict = dict()

    def table_emitters_insert(self):
        # get selected row index

        selected_indexes = self.ui.tableView_emitters.selectionModel().selectedIndexes()
        selected_row_index = selected_indexes[-1].row()
        # insert
        self.TableModel_emitters.insertRow(selected_row_index)
        self.ui.tableView_emitters.layoutChanged().emit()
        self.ui.tableView_emitters.resizeRowsToContents()
        self.repaint()

    def table_emitters_remove(self):
        if self.TableModel_emitters.rowCount(self.ui.tableView_emitters) <= 1:
            raise ValueError('Not enough rows to delete.')

        # get selected row index
        selected_indexes = self.ui.tableView_emitters.selectionModel().selectedIndexes()
        selected_row_index = selected_indexes[-1].row()
        # remove
        self.TableModel_emitters.removeRow(selected_row_index)
        self.ui.tableView_emitters.layoutChanged().emit()
        self.ui.tableView_emitters.resizeRowsToContents()
        self.repaint()


    def init_table(self):

        emitter_list_default = [
            [''] * 5,
        ]
        emitter_list_header = [
            'Name', 'Point 1', 'Point 2', 'Height', u'Q kW/m²'
        ]

        self.TableModel_emitters = TableModel(self, content=emitter_list_default, row_header=emitter_list_header)
        self.ui.tableView_emitters.setModel(self.TableModel_emitters)
        # self.ui.tableView_emitters.setFont(QtGui.QFont("Helvetica", 10))
        self.ui.tableView_emitters.resizeColumnsToContents()

        self.ui.tableView_emitters.setColumnWidth(0, (self.ui.tableView_emitters.geometry().width() - 5) * .2)
        self.ui.tableView_emitters.setColumnWidth(1, (self.ui.tableView_emitters.geometry().width() - 5) * .217)
        self.ui.tableView_emitters.setColumnWidth(2, (self.ui.tableView_emitters.geometry().width() - 5) * .217)
        self.ui.tableView_emitters.setColumnWidth(3, (self.ui.tableView_emitters.geometry().width() - 5) * .217)
        self.ui.tableView_emitters.setColumnWidth(4, (self.ui.tableView_emitters.geometry().width() - 5) * .15)
        self.ui.tableView_emitters.resizeRowsToContents()

        receiver_list_default = [
            [''] * 3,
        ]
        receiver_list_header = [
            'Name', 'Point 1', 'Point 2'
        ]

        self.TableModel_receivers = TableModel(self, content=receiver_list_default, row_header=receiver_list_header)
        self.ui.tableView_receivers.setModel(self.TableModel_receivers)
        # self.ui.tableView_receivers.setFont(QtGui.QFont("Helvetica", 10))
        self.ui.tableView_receivers.resizeColumnsToContents()

        self.ui.tableView_receivers.setColumnWidth(0, (self.ui.tableView_emitters.geometry().width() - 5) * .2)
        self.ui.tableView_receivers.setColumnWidth(1, (self.ui.tableView_emitters.geometry().width() - 5) * .217)
        self.ui.tableView_receivers.setColumnWidth(2, (self.ui.tableView_emitters.geometry().width() - 5) * .217)
        self.ui.tableView_receivers.resizeRowsToContents()

    def submit(self):

        if self.__is_first_submit:
            main_plot(main(self.solver_parameters), ax=self.ax, fig=self.figure)
            self.__is_first_submit = False
        else:
            self.ax.clear()
            main_plot(main(self.solver_parameters), ax=self.ax)

        self.update_plot()

    def example(self):

        param_dict = dict(
            emitter_list=[
                dict(
                    name='facade 1',
                    x=[0, 5],
                    y=[4, 4],
                    z=[0, 3],
                    heat_flux=168
                ),
                dict(
                    name='facade 2',
                    x=[5, 10],
                    y=[5, 5],
                    z=[0, 3],
                    heat_flux=84
                ),
                dict(
                    name='facade 3',
                    x=[10, 10],
                    y=[5, 0],
                    z=[0, 3],
                    heat_flux=84
                ),
                dict(
                    name='facade 5',
                    x=[10, 5],
                    y=[0, 0],
                    z=[0, 3],
                    heat_flux=84
                ),
                dict(
                    name='facade 4',
                    x=[5, 0],
                    y=[0, 0],
                    z=[0, 3],
                    heat_flux=168
                ),
                dict(
                    name='facade 7',
                    x=[0, 0],
                    y=[0, 4],
                    z=[0, 3],
                    heat_flux=168
                ),
            ],
            receiver_list=[
                dict(
                    name='wall 1',
                    x=[-5, 15],
                    y=[-5, -5]
                ),
                dict(
                    name='wall 2',
                    x=[15, 15],
                    y=[-5, 15]
                ),
                dict(
                    name='wall 3',
                    x=[15, -5],
                    y=[15, 15]
                ),
                dict(
                    name='wall 4',
                    x=[-5, -5],
                    y=[15, -5]
                ),
            ],
            solver_domain=dict(
                x=(-10, 20),
                y=(-10, 20),
                z=(0,)
            ),
            solver_delta=.2
        )

        # set emitter data

        self.solver_parameters = param_dict
        self.repaint()

        self.submit()

    @property
    def solver_parameters(self) -> dict:
        """parse solver_parameters:dict from ui"""

        solver_parameter_dict = dict()

        # domain, parse domain parameters
        solver_domain_x = [float(i) for i in self.ui.lineEdit_solver_x.text().split(',')]
        solver_domain_y = [float(i) for i in self.ui.lineEdit_solver_y.text().split(',')]
        solver_domain_z = [float(i) for i in self.ui.lineEdit_solver_z.text().split(',')]
        solver_delta = float(self.ui.lineEdit_solver_delta.text())
        if 'solver_domain' not in self.__solver_parameters:
            solver_parameter_dict['solver_domain'] = dict()

        solver_parameter_dict['solver_delta'] = solver_delta
        solver_parameter_dict['solver_domain']['x'] = solver_domain_x
        solver_parameter_dict['solver_domain']['y'] = solver_domain_y
        solver_parameter_dict['solver_domain']['z'] = solver_domain_z

        # emitters, parse emitter parameters
        solver_parameter_dict['emitter_list'] = self.solver_parameter_emitters
        # solver_parameter_dict['emitter_list'] = [
        #     dict(
        #         name='facade 1',
        #         x=[-10, 0],
        #         y=[-10, 0],
        #         z=[-1, 1],
        #         heat_flux=168, ),
        #     dict(
        #         name='facade 2',
        #         x=[0, 10],
        #         y=[0, -10],
        #         z=[-1, 1],
        #         heat_flux=168, ),
        # ]

        # receivers, parse receiver parameters
        solver_parameter_dict['receiver_list'] = self.solver_parameter_receivers

        return solver_parameter_dict

    @solver_parameters.setter
    def solver_parameters(self, solver_parameter_dict: dict = None):
        """map solver_parameter_dict:dict to ui."""

        # domain, parse domain parameters
        solver_domain_x = ','.join(
            f'{i:.3f}'.rstrip('0').rstrip('.') for i in solver_parameter_dict['solver_domain']['x'])
        solver_domain_y = ','.join(
            f'{i:.3f}'.rstrip('0').rstrip('.') for i in solver_parameter_dict['solver_domain']['y'])
        solver_domain_z = f'{solver_parameter_dict["solver_domain"]["z"][0]:.3f}'.rstrip('0').rstrip('.')
        solver_delta = f'{solver_parameter_dict["solver_delta"]:.3f}'.rstrip('0').rstrip('.')

        self.ui.lineEdit_solver_x.setText(solver_domain_x)
        self.ui.lineEdit_solver_y.setText(solver_domain_y)
        self.ui.lineEdit_solver_z.setText(solver_domain_z)
        self.ui.lineEdit_solver_delta.setText(solver_delta)

        # emitters, parse emitter parameters
        self.solver_parameter_emitters = solver_parameter_dict['emitter_list']

        # receivers, parse receiver parameters
        self.solver_parameter_receivers = solver_parameter_dict['receiver_list']

        self.repaint()

    @property
    def solver_parameter_emitters(self) -> list:
        """parse `emitter_list` from ui."""

        emitter_list = list()
        for emitter in self.TableModel_emitters.content:
            name, xy1, xy2, z1z2, q = emitter
            x1, y1 = xy1.split(',')
            x2, y2 = xy2.split(',')
            z1, z2 = z1z2.split(',')

            emitter_list.append(
                dict(
                    name=name,
                    x=(float(x1), float(x2)),
                    y=(float(y1), float(y2)),
                    z=(float(z1), float(z2)),
                    heat_flux=float(q)
                )
            )
        return emitter_list

    @solver_parameter_emitters.setter
    def solver_parameter_emitters(self, emitter_list: list):
        """cast `emitter_list` onto ui."""

        emitter_list_prepared = list()

        for emitter in emitter_list:
            name = emitter['name']
            x1, x2 = emitter['x']
            y1, y2 = emitter['y']
            z1, z2 = emitter['z']
            q = emitter['heat_flux']

            xy1 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x1, y1])
            xy2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x2, y2])
            z1z2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [z1, z2])
            q = f'{q:.3f}'.rstrip('0').rstrip('.')

            emitter_list_prepared.append([name, xy1, xy2, z1z2, q])

        self.TableModel_emitters.content = emitter_list_prepared
        self.ui.tableView_emitters.model().layoutChanged.emit()
        self.repaint()

    @property
    def solver_parameter_receivers(self) -> list:
        """parse `receiver_list` from ui."""

        receiver_list = list()
        for receiver in self.TableModel_receivers.content:
            name, xy1, xy2 = receiver
            x1, y1 = xy1.split(',')
            x2, y2 = xy2.split(',')

            receiver_list.append(
                dict(
                    name=name,
                    x=(float(x1), float(x2)),
                    y=(float(y1), float(y2)),
                )
            )
        return receiver_list

    @solver_parameter_receivers.setter
    def solver_parameter_receivers(self, receiver_list: list):
        """cast `receiver_list` onto ui."""

        receiver_list_prepared = list()

        for receiver in receiver_list:
            name = receiver['name']
            x1, x2 = receiver['x']
            y1, y2 = receiver['y']

            xy1 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x1, y1])
            xy2 = ','.join(f'{i:.3f}'.rstrip('0').rstrip('.') for i in [x2, y2])

            receiver_list_prepared.append([name, xy1, xy2])

        self.TableModel_receivers.content = receiver_list_prepared
        self.ui.tableView_receivers.model().layoutChanged.emit()
        self.repaint()

    def update_plot(self):

        self.figure.tight_layout()
        self.figure_canvas.draw()
        self.repaint()

    def save_figure(self):
        path_to_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption='Save Figure',
            dir='image.png'
        )

        self.figure.savefig(path_to_file, dpi=96, transparent=True)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = Dialog0406()
    app.show()
    qapp.exec_()
