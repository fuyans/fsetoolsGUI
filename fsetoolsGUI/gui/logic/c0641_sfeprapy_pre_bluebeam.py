from os.path import realpath, dirname, join

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel

from fsetoolsGUI.gui.logic.c0000_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.logic.c0000_utilities import Counter


class App(AppBaseClass):
    app_id = '0641'
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
        # self.ui.p2_layout.addWidget(QLabel('Database'), c.value, 0, 1, 1)
        # self.ui.p2_in_fp_database = QLineEdit()
        # self.ui.p2_in_fp_database.setMinimumWidth(150)
        # self.ui.p2_layout.addWidget(self.ui.p2_in_fp_database, c.value, 1, 1, 1)
        # self.ui.p2_in_fp_database_unit = QPushButton('Select')
        # self.ui.p2_in_fp_database_unit.setStyleSheet('padding-left:10px; padding-right:10px; padding-top:2px; padding-bottom:2px;')
        # self.ui.p2_layout.addWidget(self.ui.p2_in_fp_database_unit, c.count, 2, 1, 1)
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_database', 'Database file path', '...', 150, unit_obj='QPushButton')
        self.add_lineedit_set_to_grid(self.ui.p2_layout, c.count, 'p2_in_fp_bluebeam_measurements', 'Measurements file path', '...', 150, unit_obj='QPushButton')
        data_description = QLabel(
            'The measurement file should be in *.csv format containing the following columns:'
            r'<ol>'
            r'<li>Subject - indicates measurement type, e.g. COMPARTMENT, COMPARTMENT_LENGTH, WINDOW, DOOR & OCCUPANCY_TYPE'
            r'<li>Label - indicates Case name;</li>'
            r'<li>Colour - indicates compartment occupancy type;</li>'
            r'<li>Area - compartment area;</li>'
            r'<li>Length - the longest compartment fire travelling path, door or window width; and</li>'
            r'<li>Depth - compartment height.</li>'
            r'</ol>'
        )
        data_description.setWordWrap(True)
        self.ui.p2_layout.addWidget(data_description, c.count, 0, 1, 3)

        self.ui.p3_example.setText('Bluebeam toolbox')

        # =================
        # signals and slots
        # =================
        def select_database():
            self.ui.p2_in_fp_database.setText(
                realpath(QtWidgets.QFileDialog.getOpenFileName(self, 'Select database', '', 'Spreadsheet (*.csv *.xlsx)')[0])
            )

        self.ui.p2_in_fp_database_unit.clicked.connect(select_database)

    def example(self):
        from fsetoolsGUI.etc.sfeprapy_bluebeam_toolbox import xml
        fp = QtWidgets.QFileDialog.getSaveFileName(self, 'Save SFEPRAPY Bluebeam toolbox', '', '(*.btx)')[0]
        if fp:
            with open(fp, 'w+') as f:
                f.write(xml)

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

    def ok(self):

        fp_measurements = realpath(QtWidgets.QFileDialog.getOpenFileName(self, 'Select output directory', '', 'measurements (*.csv)')[0])

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
            compartment_length = df[(df['Subject'] == 'COMPARTMENT_LENGTH') & (df['Label'] == case_name)].to_dict(orient='records')
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
            # data_ = OrderedDict()
            occupancy_type = colour2occ_dict[compartment['Colour']].lower().strip()  # strip and convert to lower case to avoid potential human errors

            data_ = {
                'case_name': case_name,
                'occupancy_type': occupancy_type[0].upper() + occupancy_type[1:].lower(),
                'n_simulations': 10000,
                'probability_weight': 0,

                'room_depth': compartment_length['Length'],
                'room_height': compartment['Depth'],
                'room_floor_area': compartment['Area'],
                'room_wall_thermal_inertia': 700,

                'window_height': opening_heq,
                'window_width': opening_wt,
                'window_open_fraction_permanent': (doors_heq * doors_wt) / (opening_heq * opening_wt),
                'representative_floor_area': sum([i['Area'] for i in compartment_with_duplicates]),

                # variable values obtained from `database` based upon `occupancy_type`
                'fire_hrr_density:dist': database[occupancy_type]['fire_hrr_density:dist'],
                'fire_hrr_density:lbound': database[occupancy_type]['fire_hrr_density:lbound'],
                'fire_hrr_density:ubound': database[occupancy_type]['fire_hrr_density:ubound'],
                'fire_load_density:dist': database[occupancy_type]['fire_load_density:dist'],
                'fire_load_density:lbound': database[occupancy_type]['fire_load_density:lbound'],
                'fire_load_density:ubound': database[occupancy_type]['fire_load_density:ubound'],
                'fire_load_density:mean': database[occupancy_type]['fire_load_density:mean'],
                'fire_load_density:sd': database[occupancy_type]['fire_load_density:sd'],
                'fire_tlim': database[occupancy_type]['fire_tlim'],
                'p1': database[occupancy_type]['p1'],
                'p2': database[occupancy_type]['p2'],
                'p3': database[occupancy_type]['p3'],
                'p4': database[occupancy_type]['p4'],

                'fire_time_step': 10,
                'fire_time_duration': 10800,
                'fire_spread_speed:dist': 'uniform_',
                'fire_spread_speed:lbound': 0.005,
                'fire_spread_speed:ubound': 0.036,
                'fire_nft_limit:dist': 'norm_',
                'fire_nft_limit:lbound': 623.15,
                'fire_nft_limit:ubound': 1473.15,
                'fire_nft_limit:mean': 1323.15,
                'fire_nft_limit:sd': 93,
                'fire_combustion_efficiency:dist': 'uniform_',
                'fire_combustion_efficiency:lbound': 0.8,
                'fire_combustion_efficiency:ubound': 1,
                'window_open_fraction:dist': 'lognorm_mod_',
                'window_open_fraction:ubound': 0.9999,
                'window_open_fraction:lbound': 0.0001,
                'window_open_fraction:mean': 0.2,
                'window_open_fraction:sd': 0.2,
                'beam_position_horizontal:dist': 'uniform_',
                'beam_position_horizontal:ubound': compartment_length['Length'] * 0.9,
                'beam_position_horizontal:lbound': compartment_length['Length'] * 0.6,
                'beam_position_vertical': min(3.3, compartment['Depth']),
                'beam_cross_section_area': 0.017,
                'beam_rho': 7850,
                'protection_c': 1700,
                'protection_k': 0.2,
                'protection_protected_perimeter': 2.14,
                'protection_rho': 800,
                'solver_temperature_goal': 893.15,
                'solver_max_iter': 20,
                'solver_thickness_lbound': 0.0001,
                'solver_thickness_ubound': 0.05,
                'solver_tol': 1,
                'fire_mode': 3,
                'fire_gamma_fi_q': 1,
                'fire_t_alpha': 300,
                'room_breadth': compartment['Area'] / compartment_length['Length'],
                'phi_teq:dist': 'lognorm_',
                'phi_teq:lbound': 0.0001,
                'phi_teq:ubound': 3.,
                'phi_teq:mean': 1.,
                'phi_teq:sd': 0.25,
                'timber_charring_rate': 0.0,
                'timber_hc': 0.,
                'timber_density': 0.,
                'timber_exposed_area': 0.,
                'timber_solver_ilim': 0.,
                'timber_solver_tol': 0.,
            }

            data[case_name] = data_

            # if 0 < data[case_name]['window_open_fraction_permanent'] < 1:
            #     print(f'permenant o. frac.: {data[case_name]["window_open_fraction_permanent"]}')
            #     print(f'windows:            {windows}')
            #     print(f'doors:              {doors}')
            # print('.\n')

        data_df = pd.DataFrame.from_dict(data)
        # data_df.to_csv(join(dirname(fp_measurements), 'measurements.out.csv'))
        data_df.to_excel(join(dirname(fp_measurements), 'mcs0.xlsx'))


if __name__ == "__main__":
    import sys

    qapp = QtWidgets.QApplication(sys.argv)
    app = App(post_stats=False)
    app.show()
    qapp.exec_()
