import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel, QPushButton, QLineEdit
from collections import OrderedDict

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter
from os.path import realpath, dirname,basename, join


class App(AppBaseClass):
    app_id = '0621'
    app_name_short = 'SFEPRAPY\npre-proc.\nBluebeam'
    app_name_long = 'SFEPRAPY Bluebeam exported data pre-processor'

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
        self.ui.p2_layout.addWidget(QLabel('Database'), c.value, 0, 1, 1)
        self.ui.p2_in_distribution = QLineEdit()
        self.ui.p2_in_distribution.setMinimumWidth(150)
        self.ui.p2_layout.addWidget(self.ui.p2_in_distribution, c.value, 1, 1, 1)
        self.ui.p2_in_select_dist = QPushButton('Select')
        self.ui.p2_in_select_dist.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        self.ui.p2_layout.addWidget(self.ui.p2_in_select_dist, c.count, 2, 1, 1)
        self.ui.p3_example.setVisible(False)

        # =================
        # signals and slots
        # =================
        def select_database():
            self.ui.p2_in_distribution.setText(
                realpath(QtWidgets.QFileDialog.getOpenFileName(self, 'Select database', '', 'Spreadsheet (*.csv *.xlsx)')[0])
            )
        self.ui.p2_in_select_dist.clicked.connect(select_database)

    def example(self):
        pass

    @property
    def input_parameters(self):
        pass

    @input_parameters.setter
    def input_parameters(self, v):
        pass

    @property
    def output_parameters(self):
        pass

    @output_parameters.setter
    def output_parameters(self, v):
        pass

    def select_dir_path(self, title: str = "Select file", default_dir: str = "~/",
                        file_type: str = "Safir output file (*.out *.OUT *.txt)"):
        """select input file and copy its path to ui object"""

        # dialog to select file
        path_to_file = QtWidgets.QFileDialog.getExistingDirectory(self, title, default_dir)

        # paste the select file path to the ui object
        return path_to_file

    def ok(self):

        fp_measurements = realpath(QtWidgets.QFileDialog.getOpenFileName(self, 'Select output directory','', 'measurements (*.csv)')[0])

        df_database = pd.read_excel(join(dirname(fp_measurements), 'database.xlsx'), index_col=0)
        df_database.columns = map(str.strip, map(str.lower, df_database.columns))
        database = df_database.to_dict()

        df = pd.read_csv(join(dirname(fp_measurements), 'measurements.csv'))

        df[df['Subject'] == 'KEY'].to_dict(orient='records')
        colour2occ_dict = {v['Colour']: v['Label'] for v in df[df['Subject'] == 'OCCUPANCY_TYPE'].to_dict(orient='records')}

        case_names = list(set(df[df['Subject'] == 'COMPARTMENT']['Label'].values))
        case_names.sort()
        case_names = [i for i in case_names if '_' not in i]

        # df[(df['Subject'] == 'COMPARTMENT') & (df['Label'] == '1F01')].to_dict(orient='records')
        # df[(df['Subject'] == 'COMPARTMENT_DEPTH') & (df['Label'] == '1F01')].to_dict(orient='records')

        data = dict()
        def opening_height_and_width(ws: list, hs: list):
            if len(ws) == 0 and len(hs) == 0:
                return 0, 0

            assert len(ws) == len(hs)

            total_area = 0
            total_width = 0

            for i, w in enumerate(ws):
                h = hs[i]
                total_area = total_area + w * h
                total_width = total_width + w

            weighted_height = total_area / total_width

            return weighted_height, total_width

        for case_name in case_names:
            # --------------------------------------------
            # calculate compartment and compartment length
            # --------------------------------------------
            compartment = df[(df['Subject'] == 'COMPARTMENT') & (df['Label'] == case_name)].to_dict(orient='records')
            compartment_length = df[(df['Subject'] == 'COMPARTMENT_DEPTH') & (df['Label'] == case_name)].to_dict(orient='records')
            try:
                assert len(compartment) == 1 and len(compartment_length) == 1
            except AssertionError:
                print(case_name, len(compartment), len(compartment_length))
            compartment, compartment_length = compartment[0], compartment_length[0]

            # ------------------------------------------
            # calculation ventilation opening dimensions
            # ------------------------------------------
            windows = df[(df['Subject'] == 'WINDOW') & (df['Label'] == case_name)].to_dict(orient='records')
            doors = df[(df['Subject'] == 'DOOR') & (df['Label'] == case_name)].to_dict(orient='records')

            opening_heq, opening_wt = opening_height_and_width(
                [i['Length'] for i in windows] + [i['Length'] for i in doors],
                [i['Depth'] for i in windows] + [i['Depth'] for i in doors]
            )
            doors_heq, doors_wt = opening_height_and_width([i['Length'] for i in doors], [i['Depth'] for i in doors])

            # -----------------------------------
            # calculate representative floor area
            # -----------------------------------
            compartment_with_duplicates = df[(df['Subject'] == 'COMPARTMENT') & ((df['Label'] == case_name) | (df['Label'] == f'{case_name}_'))].to_dict(orient='records')

            # print(f'case_name:         {case_name}')
            # print(f'no. duplicates:    {len(compartment_with_duplicates)-1}')
            # print(f'no. windows:       {len(windows)}')
            # print(f'no. doors:         {len(doors)}')

            # ----------------
            # assign variables
            # ----------------
            data_ = OrderedDict()
            occupancy_type = colour2occ_dict[compartment['Colour']].lower().strip()  # strip and convert to lower case to avoid potential human errors

            data_['case_name'] = case_name
            data_['occupancy_type'] = occupancy_type[0].upper() + occupancy_type[1:].lower()
            data_['n_simulations'] = 10000
            data_['probability_weight'] = 0

            data_['room_depth'] = compartment_length['Length']
            data_['room_height'] = compartment['Depth']
            data_['room_floor_area'] = compartment['Area']
            data_['room_wall_thermal_inertia'] = 700

            data_['window_height'] = opening_heq
            data_['window_width'] = opening_wt
            data_['window_open_fraction_permanent'] = (doors_heq * doors_wt) / (opening_heq * opening_wt)
            data_['representative_floor_area'] = sum([i['Area'] for i in compartment_with_duplicates])

            # variable values obtained from `database` based upon `occupancy_type`
            data_['fire_hrr_density:dist'] = database[occupancy_type]['fire_hrr_density:dist']
            data_['fire_hrr_density:lbound'] = database[occupancy_type]['fire_hrr_density:lbound']
            data_['fire_hrr_density:ubound'] = database[occupancy_type]['fire_hrr_density:ubound']
            data_['fire_load_density:dist'] = database[occupancy_type]['fire_load_density:dist']
            data_['fire_load_density:lbound'] = database[occupancy_type]['fire_load_density:lbound']
            data_['fire_load_density:ubound'] = database[occupancy_type]['fire_load_density:ubound']
            data_['fire_load_density:mean'] = database[occupancy_type]['fire_load_density:mean']
            data_['fire_load_density:sd'] = database[occupancy_type]['fire_load_density:sd']
            data_['fire_tlim'] = database[occupancy_type]['fire_tlim']
            data_['p1'] = database[occupancy_type]['p1']
            data_['p2'] = database[occupancy_type]['p2']
            data_['p3'] = database[occupancy_type]['p3']
            data_['p4'] = database[occupancy_type]['p4']

            data_['fire_time_step'] = 10
            data_['fire_time_duration'] = 10800
            data_['fire_spread_speed:dist'] = 'uniform_'
            data_['fire_spread_speed:lbound'] = 0.005
            data_['fire_spread_speed:ubound'] = 0.036
            data_['fire_nft_limit:dist'] = 'norm_'
            data_['fire_nft_limit:lbound'] = 623.15
            data_['fire_nft_limit:ubound'] = 1473.15
            data_['fire_nft_limit:mean'] = 1323.15
            data_['fire_nft_limit:sd'] = 93
            data_['fire_combustion_efficiency:dist'] = 'uniform_'
            data_['fire_combustion_efficiency:lbound'] = 0.8
            data_['fire_combustion_efficiency:ubound'] = 1
            data_['window_open_fraction:dist'] = 'lognorm_mod_'
            data_['window_open_fraction:ubound'] = 0.9999
            data_['window_open_fraction:lbound'] = 0.0001
            data_['window_open_fraction:mean'] = 0.2
            data_['window_open_fraction:sd'] = 0.2
            data_['beam_position_horizontal:dist'] = 'uniform_'
            data_['beam_position_horizontal:ubound'] = data_['room_depth'] * 0.9
            data_['beam_position_horizontal:lbound'] = data_['room_depth'] * 0.6
            data_['beam_position_vertical'] = 3.3
            data_['beam_cross_section_area'] = 0.017
            data_['beam_rho'] = 7850
            data_['protection_c'] = 1700
            data_['protection_k'] = 0.2
            data_['protection_protected_perimeter'] = 2.14
            data_['protection_rho'] = 800
            data_['solver_temperature_goal'] = 893.15
            data_['solver_max_iter'] = 20
            data_['solver_thickness_lbound'] = 0.0001
            data_['solver_thickness_ubound'] = 0.05
            data_['solver_tol'] = 1
            data_['fire_mode'] = 3
            data_['fire_gamma_fi_q'] = 1
            data_['fire_t_alpha'] = 300
            data_['room_breadth'] = 17.57
            data_['phi_teq_:dist'] = 'lognorm_'
            data_['phi_teq_:lbound'] = 0.0001
            data_['phi_teq_:ubound'] = 3
            data_['phi_teq_:mean'] = 1
            data_['phi_teq_:sd'] = 0.25
            data_['phi_teq'] = 1
            data_['timber_charring_rate'] = 0.00
            data_['timber_hc'] = 0
            data_['timber_density'] = 0
            data_['timber_exposed_area'] = 0
            data_['timber_solver_ilim'] = 0.00
            data_['timber_solver_tol'] = 0

            data[case_name] = data_

            # if 0 < data[case_name]['window_open_fraction_permanent'] < 1:
            #     print(f'permenant o. frac.: {data[case_name]["window_open_fraction_permanent"]}')
            #     print(f'windows:            {windows}')
            #     print(f'doors:              {doors}')
            # print('.\n')

        data_df = pd.DataFrame.from_dict(data)
        data_df.to_csv(join(dirname(fp_measurements), 'measurements.out.csv'))
        data_df.to_excel(join(dirname(fp_measurements), 'mcs0.xlsx'))


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
