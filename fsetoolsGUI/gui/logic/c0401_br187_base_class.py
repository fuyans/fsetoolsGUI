import logging
from os.path import join

import fsetoolsGUI
from fsetoolsGUI.gui.logic.custom_app_template import AppBaseClass

logger = logging.getLogger('gui')


class BR187BaseClass(AppBaseClass):
    app_id = None
    app_name_short = None
    app_name_long = None

    def __init__(self, ui: callable, parent=None, *args, **kwargs):

        super().__init__(parent=parent, *args, **kwargs)

        self.ui = ui()
        self.ui.setupUi(self)

        # set up radiation figure
        self.ui.label_image_figure.setPixmap(join(fsetoolsGUI.__root_dir__, 'gui', 'images', f'{self.app_id}-1.png'))

        # set default values
        self.ui.radioButton_in_S.setChecked(True)
        self.change_mode_S_and_UA()

        # signals

        self.ui.lineEdit_in_W.textChanged.connect(self.ok_silent)
        self.ui.lineEdit_in_H.textChanged.connect(self.ok_silent)
        try:
            self.ui.lineEdit_in_w.textChanged.connect(self.ok_silent)
            self.ui.lineEdit_in_h.textChanged.connect(self.ok_silent)
        except AttributeError:
            pass
        self.ui.lineEdit_in_Q.textChanged.connect(self.ok_silent)
        self.ui.lineEdit_in_Q_crit.textChanged.connect(self.ok_silent)
        self.ui.lineEdit_in_S.textChanged.connect(self.ok_silent)
        self.ui.lineEdit_in_UA.textChanged.connect(self.ok_silent)

        self.ui.radioButton_in_S.toggled.connect(self.change_mode_S_and_UA)
        self.ui.radioButton_in_UA.toggled.connect(self.change_mode_S_and_UA)

    def example(self):

        self.ui.radioButton_in_S.setChecked(True)
        self.change_mode_S_and_UA()
        self.ui.lineEdit_in_W.setText('10')
        self.ui.lineEdit_in_H.setText('6')
        try:
            self.ui.lineEdit_in_w.setText('0')
            self.ui.lineEdit_in_h.setText('0')
        except AttributeError:
            pass
        self.ui.lineEdit_in_Q.setText('84')
        self.ui.lineEdit_in_Q_crit.setText('12.6')
        self.ui.lineEdit_in_S.setText('1')

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.radioButton_in_S.isChecked():  # to calculate unprotected area percentage
            self.ui.lineEdit_in_UA.setEnabled(False)  # disable UA related inputs
            self.ui.label_in_UA_unit.setEnabled(False)  # disable UA related inputs
            self.ui.lineEdit_in_S.setEnabled(True)  # enable S related inputs
            self.ui.label_in_S_unit.setEnabled(True)  # enable S related inputs
            self.ui.label_out_S_or_UA.setText('Allowable unprotected area')
            self.ui.label_out_S_or_UA_unit.setText('%')
            self.ui.label_out_S_or_UA.setToolTip('Solved maximum permitted unprotected area')
        elif self.ui.radioButton_in_UA.isChecked():  # to calculate separation to boundary
            self.ui.lineEdit_in_S.setEnabled(False)  # disable S related inputs
            self.ui.label_in_S_unit.setEnabled(False)  # disable S related inputs
            self.ui.lineEdit_in_UA.setEnabled(True)  # enable UA related inputs
            self.ui.label_in_UA_unit.setEnabled(True)  # enable UA related inputs
            self.ui.label_out_S_or_UA.setText('½S, min. sep. distance')
            self.ui.label_out_S_or_UA_unit.setText('m')
            self.ui.label_out_S_or_UA.setToolTip('Solved minimum separation distance to boundary.')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.lineEdit_out_Phi.setText('')
        self.ui.lineEdit_out_q.setText('')
        self.ui.lineEdit_out_S_or_UA.setText('')

        self.repaint()

    @property
    def input_parameters(self) -> dict:
        """parse input parameters from the ui"""

        # assign default values
        W, H, w, h, S, UA, Q, Q_a = [None] * 8

        # W - emitter width
        # H - emitter height
        # w - receiver location horizontal
        # h - receiver location vertical
        # S - separation distance
        # UA - unprotected area
        # Q - emitter heat flux
        # Q_a - acceptable heat flux or critical heat flux

        # a helper function to transform string to float with error handling
        def str2float(str: str):
            try:
                return float(str)
            except ValueError:
                return None

        # parse input parameters from ui
        W = str2float(self.ui.lineEdit_in_W.text())
        H = str2float(self.ui.lineEdit_in_H.text())
        try:
            w = str2float(self.ui.lineEdit_in_w.text())
            h = str2float(self.ui.lineEdit_in_h.text())
        except:
            pass
        if self.ui.radioButton_in_S.isChecked():
            S = str2float(self.ui.lineEdit_in_S.text())
            if S:
                # convert surface to relevant boundary to surface to surface distance
                S *= 2.
        elif self.ui.radioButton_in_UA.isChecked():
            UA = str2float(self.ui.lineEdit_in_UA.text())
            if UA is not None:
                # convert % to absolute i.e. 98% -> 0.98
                UA /= 100.
            else:
                raise ValueError('Unknown format, unprotected area input parameter should be a positive float')

        Q = str2float(self.ui.lineEdit_in_Q.text())
        Q_a = str2float(self.ui.lineEdit_in_Q_crit.text())

        # validate input values
        self.validate(W, 'unsigned float', 'Emitter width should be greater than 0')
        self.validate(H, 'unsigned float', 'Emitter height should be greater than 0')
        if self.app_id == '0403' or self.app_id == '0404':
            self.validate(w, float, 'Receiver offset "w" should be a number')
            self.validate(h, float, 'Receiver offset "h" should be a number')
        # THE BELOW IS REMOVED ON 05/06/2020
        # THE PURPOSE OF THIS TOOL IS ONLY TO CALCULATION RADIATION HEAT TRANSFER, NOT TO CHECK AGAINST ADB ETC
        # if S:
        #     try:
        #         # check if S provided is greater than S (1 m to the relevant boundary)
        #         assert S >= 2
        #     except AssertionError:
        #         raise ValueError('Separation to relevant boundary should be greater than 1 m')
        if UA is not None:
            try:
                assert all((UA > 0, UA <= 1))
            except AssertionError:
                raise ValueError('Unprotected area should be greater than 0 and less than 100 %')

        self.validate(Q_a, 'unsigned float', 'Receiver critical heat flux should be greater than 0')
        self.validate(Q, 'unsigned float', 'Emitter heat flux should be greater than 0')

        # check if enough inputs are provided for any calculation options
        try:
            if self.app_id == '0403' or self.app_id == '0404':
                assert all(i is not None for i in (W, H, w, h))
            else:
                assert all(i is not None for i in (W, H))

            assert UA is not None or S is not None

            if UA is not None:
                # if to calculate the required separation S for a given UA,
                # then Q is also required
                assert Q
        except AssertionError:
            raise ValueError('Not enough input parameters')

        return dict(W=W, H=H, w=w, h=h, S=S, UA=UA, Q_a=Q_a, Q=Q)

    @property
    def output_parameters(self) -> dict:
        return dict()  # currently not used

    # @staticmethod
    # def phi_solver(W: float, H: float, w: float, h: float, Q: float, Q_a: float, S=None, UA=None) -> tuple:
    #     """
    #     :param W: Emitter width
    #     :param H: Emitter height
    #     :param w: Receiver loc 1 (along width axis)
    #     :param h: Receiver loc 2 (along height axis)
    #     :param Q: Emitter heat flux
    #     :param Q_a: Receiver acceptable heat flux
    #     :param S: Separation distance between emitter and receiver
    #     :param UA: Unprotected area
    #     :return:
    #     """
    #     return tuple()

    @output_parameters.setter
    def output_parameters(self, v: dict):
        try:
            assert all([i in v for i in ('phi', 'q', 'UA', 'S')])
            phi, q, UA, S = v['phi'], v['q'], v['UA'], v['S']
        except KeyError:
            raise KeyError('Not enough output parameters')

        self.ui.lineEdit_out_Phi.setText(f'{phi * 1000:.2f}')
        self.ui.lineEdit_out_q.setText(f'{q:.2f}')

        if S:
            self.ui.lineEdit_out_S_or_UA.setText(f'{S / 2:.2f}')
        elif UA:
            self.ui.lineEdit_out_S_or_UA.setText(f'{UA * 100:.2f}')

    def calculate(self):

        # clear ui output fields
        self.ui.lineEdit_out_S_or_UA.clear()
        self.ui.lineEdit_out_Phi.clear()
        self.ui.lineEdit_out_q.clear()

        # --------------------
        # Parse inputs from ui
        # --------------------
        try:
            input_parameters = self.input_parameters
        except Exception as e:
            raise e

        # -----------
        # Calculation
        # -----------
        try:
            phi, q, S, UA, msg = self.phi_solver(**input_parameters)
        except Exception as e:
            raise e

        # --------------
        # Assign outputs
        # --------------
        try:
            self.output_parameters = dict(phi=phi, q=q, S=S, UA=UA)
        except Exception as e:
            raise e

    def ok_silent(self):
        try:
            self.calculate()
            self.repaint()
        except Exception as e:
            logger.debug(e)

    def ok(self):
        try:
            self.calculate()
            self.repaint()
        except Exception as e:
            logger.error(f'{e}')
            self.statusBar().showMessage(f'{e}')
            self.repaint()
            return

    def __init_subclass__(cls, **kwargs):
        try:
            assert hasattr(cls, 'phi_solver')
        except AssertionError:
            raise AttributeError('phi_solver not defined in subclass')
