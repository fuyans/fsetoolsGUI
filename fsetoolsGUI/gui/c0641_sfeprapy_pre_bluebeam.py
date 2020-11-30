import copy
from os.path import realpath, dirname, join

import pandas as pd
from PySide2 import QtWidgets
from PySide2.QtWidgets import QGridLayout, QLabel
from sfeprapy.func.mcs_gen import dict_flatten
from sfeprapy.mcs0 import EXAMPLE_INPUT_DICT

from fsetoolsGUI import logger
from fsetoolsGUI.gui.c9901_app_template import AppBaseClass, AppBaseClassUISimplified01
from fsetoolsGUI.gui.custom_utilities import Counter


class App(AppBaseClass):
    app_id = '0641'
    app_name_short = 'PRAPY MCS0\npre-proc.\nBluebeam'
    app_name_long = 'SFEPRAPY MCS0 Bluebeam exported data pre-processor'

    def __init__(self, parent=None, post_stats: bool = True):

        # ================================
        # instantiation super and setup ui
        # ================================
        super().__init__(parent, post_stats, ui=AppBaseClassUISimplified01)
        self.__database = None
        self.__measurements = None

        # ================
        # instantiation ui
        # ================
        c = Counter()
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setVerticalSpacing(5), self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), c.count, 0, 1, 3)
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
        self.ui.p2_in_fp_database_unit.clicked.connect(
            lambda: self.get_open_file_name('Select database', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_database.setText)
        )
        self.ui.p2_in_fp_bluebeam_measurements_unit.clicked.connect(
            lambda: self.get_open_file_name('Select measurements file', 'Spreadsheet (*.csv *.xlsx)', func_to_assign_fp=self.ui.p2_in_fp_bluebeam_measurements.setText)
        )

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

        fp_measurements = realpath(self.ui.p2_in_fp_bluebeam_measurements.text())
        fp_database = realpath(self.ui.p2_in_fp_database.text())

        df_database = pd.read_excel(fp_database, index_col=0)
        df_database.columns = map(str.strip, map(str.lower, df_database.columns))
        database = df_database.to_dict()

        df = pd.read_csv(fp_measurements, thousands=r',')

        df[['Length', 'Area', 'Depth']] = df[['Length', 'Area', 'Depth']].apply(pd.to_numeric)

        df[df['Subject'] == 'KEY'].to_dict(orient='records')
        colour2occ_dict = {v['Colour']: v['Label'] for v in df[df['Subject'] == 'OCCUPANCY_TYPE'].to_dict(orient='records')}

        case_names = list()
        for case_name in sorted(list(set(df[df['Subject'] == 'COMPARTMENT']['Label'].values))):
            if not str(case_name).endswith('_'):
                case_names.append(case_name)

        # df[(df['Subject'] == 'COMPARTMENT') & (df['Label'] == '1F01')].to_dict(orient='records')
        # df[(df['Subject'] == 'COMPARTMENT_DEPTH') & (df['Label'] == '1F01')].to_dict(orient='records')

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

        data_dict: dict = dict()
        for case_name in case_names:
            logger.info(f'Processing {case_name} ...')

            # --------------------------------------------
            # calculate compartment and compartment length
            # --------------------------------------------
            compartment = df[(df['Subject'] == 'COMPARTMENT') & (df['Label'] == case_name)].to_dict(orient='records')
            try:
                assert len(compartment) == 1
            except AssertionError:
                logger.warning(f'Duplicated compartment name detected: {case_name} = {len(compartment)}')
            compartment = compartment[0]

            # ------------------------------------------
            # calculation ventilation opening dimensions
            # ------------------------------------------
            windows = df[(df['Subject'] == 'WINDOW') & (df['Label'] == case_name)].to_dict(orient='records')
            doors = df[(df['Subject'] == 'DOOR') & (df['Label'] == case_name)].to_dict(orient='records')
            logger.info(f'Total number of glazed openings: {len(windows)}')
            logger.info(f'Total number of doors: {len(doors)}')

            opening_heq, opening_wt = opening_height_and_width(
                [i['Length'] for i in windows] + [i['Length'] for i in doors],
                [i['Depth'] for i in windows] + [i['Depth'] for i in doors]
            )
            logger.info(f'Total glazed opening height: {opening_heq}')
            logger.info(f'Total glazed opening width: {opening_wt}')

            doors_heq, doors_wt = opening_height_and_width([i['Length'] for i in doors], [i['Depth'] for i in doors])
            logger.info(f'Total door opening height: {doors_heq}')
            logger.info(f'Total door opening width: {doors_wt}')

            window_open_fraction_permanent = (doors_heq * doors_wt) / (opening_heq * opening_wt)
            logger.info(f'Permanent ventilation opening fraction: {window_open_fraction_permanent}')

            # ----------------------------
            # calculate general floor area
            # ----------------------------
            compartment_with_duplicates = df[(df['Subject'] == 'COMPARTMENT') & ((df['Label'] == case_name) | (df['Label'] == f'{case_name}_'))].to_dict(orient='records')

            # ----------------
            # assign variables
            # ----------------
            # data_ = OrderedDict()
            occupancy_type = colour2occ_dict[compartment['Colour']].lower().strip()  # strip and convert to lower case to avoid potential human errors

            room_depth = df[(df['Subject'] == 'COMPARTMENT_LENGTH') & (df['Label'] == case_name)].to_dict(orient='records')
            room_depth = sum([v['Length'] for v in room_depth])

            room_floor_area = compartment['Area']
            room_height = compartment['Depth']
            room_breadth = room_floor_area / room_depth

            general_room_floor_area = sum([i['Area'] for i in compartment_with_duplicates])

            data_ = EXAMPLE_INPUT_DICT['Standard Case 1']

            data_.update(dict(
                case_name=case_name,
                occupancy_type=occupancy_type[0].upper() + occupancy_type[1:].lower(),
                room_depth=room_depth,
                room_breadth=room_breadth,
                room_height=room_height,
                room_floor_area=room_floor_area,
                window_height=opening_heq,
                window_width=opening_wt,
                window_open_fraction_permanent=window_open_fraction_permanent,
                general_room_floor_area=general_room_floor_area,
                fire_hrr_density=dict(
                    dist=database[occupancy_type]['fire_hrr_density:dist'],
                    ubound=database[occupancy_type]['fire_hrr_density:ubound'],
                    lbound=database[occupancy_type]['fire_hrr_density:lbound'],
                ),
                fire_load_density=dict(
                    dist=database[occupancy_type]['fire_load_density:dist'],
                    ubound=database[occupancy_type]['fire_load_density:ubound'],
                    lbound=database[occupancy_type]['fire_load_density:lbound'],
                    mean=database[occupancy_type]['fire_load_density:mean'],
                    sd=database[occupancy_type]['fire_load_density:sd'],
                ),
                p1=1,
                p2=1,
                p3=1,
                p4=1,
                beam_position_horizontal=dict(dist='uniform_', ubound=0.9 * room_depth, lbound=0.6 * room_depth),
                beam_position_vertical=min(3.3, room_height),
            ))

            data_dict[case_name] = dict_flatten(data_)

        data_df = pd.DataFrame.from_dict(data_dict)
        data_df.to_excel(join(dirname(fp_measurements), 'mcs0.xlsx'))


def measurements_to_inputs(
        df_measurements: pd.DataFrame,
        df_predefined: pd.DataFrame
):
    def str2float(str_: str):
        try:
            return float(str_)
        except ValueError:
            return str_

    output_dict = dict()
    for case in df_measurements.to_dict(orient='records'):
        occupancy_type = case.pop('occupancy_type')

        room_depth = case['room_depth']
        room_height = case['room_height']
        room_floor_area = case['room_floor_area']
        # calculate `room_breadth`
        case['room_breadth'] = room_floor_area / room_depth
        # calculate `beam_position_horizontal`
        case['beam_position_horizontal:dist'] = 'uniform_'
        case['beam_position_horizontal:ubound'] = room_depth * 0.6
        case['beam_position_horizontal:lbound'] = room_depth * 0.9
        # calculate `beam_position_vertical`
        case['beam_position_vertical'] = min(3.3, room_height)

        # parse pre-defined parameters
        data = df_predefined[occupancy_type].to_dict()

        # update inputs with pre-defined parameters
        for k, v in data.items():
            if not k in case.keys() or not k.split(':')[0] in case.keys():
                case[k] = str2float(v)

        # add processed case
        output_dict[case['case_name']] = copy.copy(case)

    df_output = pd.DataFrame.from_dict(output_dict)

    return df_output


if __name__ == "__main__":
    # import sys
    # qapp = QtWidgets.QApplication(sys.argv)
    # app = App(post_stats=False)
    # app.show()
    # qapp.exec_()

    res = measurements_to_inputs(
        df_measurements=pd.read_csv(r'C:\Users\IanFu\Desktop\New folder\trial_01_without_timber\!measurements.csv'),
        df_predefined=pd.read_csv(r'C:\Users\IanFu\Desktop\New folder\trial_01_without_timber\!predefined.csv', index_col=0)
    )

    print(res)
    res.to_excel(r'C:\Users\IanFu\Desktop\New folder\trial_01_without_timber\0-mcs0_inputs.xlsx')
