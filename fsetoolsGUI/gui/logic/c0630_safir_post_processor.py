import os.path as path

from PySide2 import QtWidgets, QtCore

from fsetoolsGUI.etc.safir_post_processor import out2pstrain, pstrain2dict, save_csv, make_strain_lines_for_given_shell
from fsetoolsGUI.gui.layout.i0630_safir_postprocessor import Ui_MainWindow
from fsetoolsGUI.gui.logic.custom_mainwindow import QMainWindow
from fsetoolsGUI.gui.logic.custom_plot import App as PlotApp
from fsetoolsGUI.gui.logic.custom_table import TableWindow


class App0630(QMainWindow):
    __output_fire_curve = dict(
        time=None,
        temperature=None
    )

    def __init__(self, parent=None, mode=None):
        module_id = '0630'
        self.__dict_out = None
        self.__Table = None
        self.__Figure = None
        self.__Figure_ax = None
        self.__fp_out = None
        self.__dir_work = None
        self.__fp_out_processed = None
        self.__strain_lines = None

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(
            module_id=module_id,
            parent=parent,
            freeze_window_size=False,
            mode=mode
        )
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init(self)

        # =======================
        # lineEdit default values
        # =======================
        self.ui.lineEdit_in_fp_out.setReadOnly(True)
        # self.ui.lineEdit_in_initial_temperature.setText('20')

        # =================
        # lineEdit tip text
        # =================
        # self.ui.lineEdit_in_duration.setToolTip('Fire duration')

        # signals
        # self.ui.pushButton_example.clicked.connect(self.example)
        self.ui.pushButton_fp_out.clicked.connect(self.upon_output_file_selection)
        self.ui.comboBox_in_shell.currentIndexChanged.connect(self.__upon_shell_combobox_change)

    @property
    def input_parameters(self):

        def str2int(v):
            try:
                return int(v)
            except:
                return None

        # ====================
        # parse values from ui
        # ====================
        fp_out = self.ui.lineEdit_in_fp_out.text()
        unique_shell = str2int(self.ui.lineEdit_in_shell.text())

        # ======================================================
        # check if necessary inputs are provided for calculation
        # ======================================================

        # ==============================
        # validate individual parameters
        # ==============================

        # ================
        # units conversion
        # ================

        return dict(fp_out=fp_out, unique_shell=unique_shell)

    @input_parameters.setter
    def input_parameters(self, v):

        def num2str(num):
            if isinstance(num, int):
                return f'{num:g}'
            elif isinstance(num, float):
                return f'{num:.3f}'.rstrip('0').rstrip('.')
            elif isinstance(num, str):
                return v
            elif num is None:
                return ''
            else:
                return str(v)

        # units conversion
        v['duration'] /= 60  # seconds -> minutes
        v['fire_limiting_time'] /= 60  # seconds -> minutes
        v['initial_temperature'] -= 273.15  # degree Kelvin -> degree Celsius

        self.ui.lineEdit_in_duration.setText(num2str(v['duration']))
        self.ui.lineEdit_in_room_total_surface_area.setText(num2str(v['room_total_surface_area']))
        self.ui.lineEdit_in_room_floor_area.setText(num2str(v['room_floor_area']))
        self.ui.lineEdit_in_ventilation_area.setText(num2str(v['ventilation_area']))
        self.ui.lineEdit_in_ventilation_opening_height.setText(num2str(v['ventilation_opening_height']))
        self.ui.lineEdit_in_fuel_density.setText(num2str(v['fuel_density']))
        self.ui.lineEdit_in_lining_thermal_conductivity.setText(num2str(v['lining_thermal_conductivity']))
        self.ui.lineEdit_in_lining_density.setText(num2str(v['lining_density']))
        self.ui.lineEdit_in_lining_thermal_heat_capacity.setText(num2str(v['lining_thermal_heat_capacity']))
        self.ui.lineEdit_in_fire_limiting_time.setText(num2str(v['fire_limiting_time']))
        self.ui.lineEdit_in_initial_temperature.setText(num2str(v['initial_temperature']))

    @property
    def output_parameters(self):
        return self.__output_fire_curve

    @output_parameters.setter
    def output_parameters(self, v):
        self.__output_fire_curve['time'] = v['time']
        self.__output_fire_curve['temperature'] = v['temperature']

    def upon_output_file_selection(self):
        self.statusBar().showMessage('Processing...')

        fp_out = self.select_file_path()
        if not fp_out:
            self.statusBar().showMessage('Nothing selected.')

        self.__fp_out = fp_out
        self.__dir_work = path.dirname(self.__fp_out)
        self.__fp_out_processed = path.join(self.__dir_work, path.basename(self.__fp_out) + '.p')

        out2pstrain(self.__fp_out, self.__fp_out_processed)

        self.__dict_out = pstrain2dict(self.__fp_out_processed)

        list_unique_shell = list(set(self.__dict_out['list_shell']))
        list_unique_shell.sort()
        list_unique_shell = [f'{i:g}' for i in list_unique_shell]
        self.ui.comboBox_in_shell.clear()
        self.ui.comboBox_in_shell.addItems(list_unique_shell)

        save_csv(path.join(self.__dir_work, path.basename(self.__fp_out) + '.strain.csv'), **self.__dict_out)

        self.statusBar().showMessage('*.out file processed.')

    def __upon_shell_combobox_change(self):
        self.ui.lineEdit_in_shell.setText(self.ui.comboBox_in_shell.currentText())

    def ok(self):

        # clear ui output fields
        # none

        # parse inputs from ui
        input_parameters = self.input_parameters

        # calculate
        self.__strain_lines = make_strain_lines_for_given_shell(input_parameters['unique_shell'], **self.__dict_out)

        # cast outputs to ui
        self.show_results_in_figure()
        self.show_results_in_table()
        self.statusBar().showMessage('Calculation complete')
        self.repaint()

    def make_figure_and_table(self, unique_shell: int, **kwargs):
        self.__strain_lines = make_strain_lines_for_given_shell(**kwargs)

    def select_file_path(self):
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select File",
            "~/",
            "Safir output file (*.out *.OUT *.txt)")

        # paste the select file path to the ui object
        return path_to_file

    def show_results_in_table(self):

        # output_parameters = self.output_parameters

        list_x = [list(i['x']) for i in self.__strain_lines]
        list_y = [i['y'] for i in self.__strain_lines]
        list_label = [i['label'] for i in self.__strain_lines]

        # make a full x values
        x_all = []
        for i in self.__strain_lines:
            x_all += list(i['x'])
        x_all = list(set(x_all))
        x_all.sort()

        # fill y values to match len(x_all)
        for i in range(len(list_x)):
            x = list_x[i]
            y = list_y[i]
            y_ = [0] * len(x_all)
            for j, v in enumerate(x_all):
                try:
                    y_[j] = y[x.index(v)]
                except ValueError:
                    pass
            list_y[i] = y_
            print(len(y_))

        list_content = [x_all]
        [list_content.append(i) for i in list_y]
        list_content = [[float(j) for j in i] for i in zip(*list_content)]

        # print results (for console enabled version only)

        try:
            win_geo = self.__Table.geometry()
            self.__Table.destroy(destroyWindow=True, destroySubWindows=True)
            del self.__Table
        except AttributeError as e:
            win_geo = None

        self.__Table = TableWindow(
            parent=self,
            window_geometry=win_geo,
            data_list=list_content,
            header_col=['time'] + list_label,
            window_title='Parametric fire numerical results',
        )

        self.__Table.TableModel.sort(0, QtCore.Qt.AscendingOrder)
        self.__Table.TableView.resizeColumnsToContents()
        self.__Table.show()

        return True

    def show_results_in_figure(self):

        # output_parameters = self.output_parameters

        if self.__Figure is None:
            self.__Figure = PlotApp(self, title='Parametric fire plot')
            self.__Figure_ax = self.__Figure.add_subplots()
        else:
            self.__Figure_ax.clear()

        for i in self.__strain_lines:
            self.__Figure_ax.plot(i['x'] / 60, i['y'], label=i['label'])

        self.__Figure_ax.set_xlabel('Time [minute]')
        self.__Figure_ax.set_ylabel('Strain')
        self.__Figure_ax.legend(shadow=False, edgecolor='k', fancybox=False, ncol=1, fontsize='small').set_visible(True)
        self.__Figure.figure.tight_layout()

        self.__Figure.figure_canvas.draw()
        self.__Figure.show()

        return True


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App0630(mode=-1)
    app.show()
    qapp.exec_()
