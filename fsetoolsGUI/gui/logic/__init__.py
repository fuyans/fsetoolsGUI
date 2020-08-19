from os import path

from fsetoolsGUI import __root_dir__
from fsetoolsGUI.gui.logic.c0101_adb_data_sheet_1 import App as App0101
from fsetoolsGUI.gui.logic.c0102_bs9999_data_sheet_1 import App as App0102
from fsetoolsGUI.gui.logic.c0103_bs9999_merging_flow import App as App0103
from fsetoolsGUI.gui.logic.c0104_adb_merging_flow import App as App0104
from fsetoolsGUI.gui.logic.c0111_pd7974_detector_activation import App as App0111
from fsetoolsGUI.gui.logic.c0401_br187_parallel_simple import App as App0401
from fsetoolsGUI.gui.logic.c0402_br187_perpendicular_simple import App as App0402
from fsetoolsGUI.gui.logic.c0403_br187_parallel_complex import App as App0403
from fsetoolsGUI.gui.logic.c0404_br187_perpendicular_complex import App as App0404
from fsetoolsGUI.gui.logic.c0405_tra_3d_point import App as App0405
from fsetoolsGUI.gui.logic.c0406_tra_2d_xy_contour import App as App0406
from fsetoolsGUI.gui.logic.c0407_tra_enclosure import App as App0407
from fsetoolsGUI.gui.logic.c0601_naming_convention import App as App0601
from fsetoolsGUI.gui.logic.c0602_pd7974_flame_height import App as App0602
from fsetoolsGUI.gui.logic.c0611_parametric_fire import App as App0611
from fsetoolsGUI.gui.logic.c0620_probability_distribution import App as App0620
from fsetoolsGUI.gui.logic.c0630_safir_post_processor import App as App0630
from fsetoolsGUI.gui.logic.c0701_aws_s3_uploader import App as App0701


class Apps:
    __apps = {
        '0101': App0101,
        '0102': App0102,
        '0103': App0103,
        '0104': App0104,
        '0111': App0111,
        '0401': App0401,
        '0402': App0402,
        '0403': App0403,
        '0404': App0404,
        '0405': App0405,
        '0406': App0406,
        '0407': App0407,
        '0601': App0601,
        '0602': App0602,
        '0611': App0611,
        '0620': App0620,
        '0630': App0630,
        '0701': App0701,
    }

    def __init__(self):
        pass

    def app_name_long(self, code: str):
        try:
            return self.__apps[code].app_name_long
        except AttributeError:
            return None

    def app_name_short(self, code: str):
        try:
            return self.__apps[code].app_name_short
        except AttributeError:
            return None

    def app_name_short_and_long(self, code: str):
        return f'{self.app_name_short(code)}', f'{self.app_name_long(code)}'

    def doc_file_path(self, code: str):
        return path.join(__root_dir__, 'gui', 'docs', f'{code}.html')

    def doc_html(self, code: str):
        with open(self.doc_file_path(code), 'r') as f:
            return f.read()

    def print_all_app_info(self):
        module_code = list(self.__apps.keys())
        module_app_name_long = list()

        l1, l2 = 0, 0
        for i in self.__apps:
            module_app_name_long.append(self.__apps[i].app_name_long)

            if l1 < len(i):
                l1 = len(i)
            if l2 < len(module_app_name_long[-1]):
                l2 = len(module_app_name_long[-1])

        return '\n'.join([f'{i:<{l1}}     {j:<{l2}}' for i, j in zip(module_code, module_app_name_long)])

    def activate_app(self, code: str, parent=None):
        app = self.__apps[code](parent=parent)
        app.show()
        return app


if __name__ == '__main__':
    apps = Apps()
    print(apps.print_all_app_info())
