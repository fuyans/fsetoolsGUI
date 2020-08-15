import logging

from PySide2.QtWidgets import QLabel, QGridLayout

from fsetoolsGUI.gui.logic.custom_app_template_1 import AppBaseClass

logger = logging.getLogger('gui')


class BR187SimpleBaseClass(AppBaseClass):
    app_id = None
    app_name_short = None
    app_name_long = None

    def __init__(self, parent=None, post_stats: bool = True, *args, **kwargs):
        super().__init__(parent=parent, post_stats=post_stats, *args, **kwargs)
        self.init_ui()

        # set default values
        self.ui.p2_in_half_S_label.setChecked(True)
        self.change_mode_S_and_UA()

        # signals
        self.ui.p2_in_W.textChanged.connect(self.ok_silent)
        self.ui.p2_in_H.textChanged.connect(self.ok_silent)
        self.ui.p2_in_Q.textChanged.connect(self.ok_silent)
        self.ui.p2_in_Q_crit.textChanged.connect(self.ok_silent)
        self.ui.p2_in_half_S.textChanged.connect(self.ok_silent)
        self.ui.p2_in_unprotected_area.textChanged.connect(self.ok_silent)

        self.ui.p2_in_half_S_label.toggled.connect(self.change_mode_S_and_UA)
        self.ui.p2_in_unprotected_area_label.toggled.connect(self.change_mode_S_and_UA)

    def init_ui(self):

        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 1)
        self.add_widget_to_grid(self.ui.p2_layout, 1, 'p2_in_W', 'W, emitter width', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 2, 'p2_in_H', 'H, emitter height', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 3, 'p2_in_Q', 'Emitter heat flux', 'kW/m<sup>2</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 4, 'p2_in_Q_crit', 'Receiver critical heat flux', 'kW/m<sup>2</sup>')
        self.add_widget_to_grid(
            self.ui.p2_layout, 5, 'p2_in_half_S', '½S, emitter to boundary', 'm', descrip_cls='QRadioButton')
        self.add_widget_to_grid(
            self.ui.p2_layout, 6, 'p2_in_unprotected_area', 'Unprotected option', '%', descrip_cls='QRadioButton')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 7, 0, 1, 1)
        self.add_widget_to_grid(self.ui.p2_layout, 8, 'p2_out_Phi', 'Φ, configuration factor', '×10<sup>-3</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 9, 'p2_out_q', 'q, receiver heat flux', 'kW/m<sup>2</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 10, 'p2_out_S_or_UA', 'Allowable unprotected area', '%')

    def example(self):
        self.ui.p2_in_half_S_label.setChecked(True)
        self.change_mode_S_and_UA()
        self.ui.p2_in_W.setText('10')
        self.ui.p2_in_H.setText('6')
        self.ui.p2_in_Q.setText('84')
        self.ui.p2_in_Q_crit.setText('12.6')
        self.ui.p2_in_half_S.setText('1')

        self.repaint()

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.p2_in_half_S_label.isChecked():  # to calculate unprotected area percentage
            self.ui.p2_in_unprotected_area.setEnabled(False)  # disable UA related inputs
            self.ui.p2_in_unprotected_area_unit.setEnabled(False)  # disable UA related inputs
            self.ui.p2_in_half_S.setEnabled(True)  # enable S related inputs
            self.ui.p2_in_half_S_unit.setEnabled(True)  # enable S related inputs
            self.ui.p2_out_S_or_UA_label.setText('Allowable unprotected area')
            self.ui.p2_out_S_or_UA_unit.setText('%')
            self.ui.p2_out_S_or_UA.setToolTip('Solved maximum permitted unprotected area')
        elif self.ui.p2_in_unprotected_area_label.isChecked():  # to calculate separation to boundary
            self.ui.p2_in_half_S.setEnabled(False)  # disable S related inputs
            self.ui.p2_in_half_S_unit.setEnabled(False)  # disable S related inputs
            self.ui.p2_in_unprotected_area.setEnabled(True)  # enable UA related inputs
            self.ui.p2_in_unprotected_area_unit.setEnabled(True)  # enable UA related inputs
            self.ui.p2_out_S_or_UA_label.setText('½S, min. sep. distance')
            self.ui.p2_out_S_or_UA_unit.setText('m')
            self.ui.p2_out_S_or_UA.setToolTip('Solved minimum separation distance to boundary.')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.p2_out_Phi.setText('')
        self.ui.p2_out_q.setText('')
        self.ui.p2_out_S_or_UA.setText('')

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
        def str2float(v_: str):
            try:
                return float(v_)
            except ValueError:
                return None

        # parse input parameters from ui
        W = str2float(self.ui.p2_in_W.text())
        H = str2float(self.ui.p2_in_H.text())
        if self.ui.p2_in_half_S_label.isChecked():
            S = str2float(self.ui.p2_in_half_S.text())
            if S:
                # convert surface to relevant boundary to surface to surface distance
                S *= 2.
        elif self.ui.p2_in_unprotected_area_label.isChecked():
            UA = str2float(self.ui.p2_in_unprotected_area.text())
            if UA is not None:
                # convert % to absolute i.e. 98% -> 0.98
                UA /= 100.
            else:
                raise ValueError('Unknown format, unprotected area input parameter should be a positive float')

        Q = str2float(self.ui.p2_in_Q.text())
        Q_a = str2float(self.ui.p2_in_Q_crit.text())

        # validate input values
        self.validate(W, 'unsigned float', 'Emitter width should be greater than 0')
        self.validate(H, 'unsigned float', 'Emitter height should be greater than 0')
        if UA is not None:
            try:
                assert all((UA > 0, UA <= 1))
            except AssertionError:
                raise ValueError('Unprotected area should be greater than 0 and less than 100 %')

        self.validate(Q_a, 'unsigned float', 'Receiver critical heat flux should be greater than 0')
        self.validate(Q, 'unsigned float', 'Emitter heat flux should be greater than 0')

        # check if enough inputs are provided for any calculation options
        try:
            assert W is not None and H is not None
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

        self.ui.p2_out_Phi.setText(f'{phi * 1000:.2f}')
        self.ui.p2_out_q.setText(f'{q:.2f}')

        if S:
            self.ui.p2_out_S_or_UA.setText(f'{S / 2:.2f}')
        elif UA:
            self.ui.p2_out_S_or_UA.setText(f'{UA * 100:.2f}')

    def ok(self):
        pass

    def calculate(self):

        # clear ui output fields
        self.ui.p2_out_S_or_UA.clear()
        self.ui.p2_out_Phi.clear()
        self.ui.p2_out_q.clear()

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


class BR187ComplexBaseClass(AppBaseClass):
    app_id = None
    app_name_short = None
    app_name_long = None

    def __init__(self, parent=None, post_stats: bool = True, *args, **kwargs):
        super().__init__(parent=parent, post_stats=post_stats, *args, **kwargs)
        self.init_ui()

        # set default values
        self.ui.p2_in_half_S_label.setChecked(True)
        self.change_mode_S_and_UA()

        # signals
        self.ui.p2_in_W.textChanged.connect(self.ok_silent)
        self.ui.p2_in_H.textChanged.connect(self.ok_silent)
        self.ui.p2_in_Q.textChanged.connect(self.ok_silent)
        self.ui.p2_in_Q_crit.textChanged.connect(self.ok_silent)
        self.ui.p2_in_half_S.textChanged.connect(self.ok_silent)
        self.ui.p2_in_unprotected_area.textChanged.connect(self.ok_silent)

        self.ui.p2_in_half_S_label.toggled.connect(self.change_mode_S_and_UA)
        self.ui.p2_in_unprotected_area_label.toggled.connect(self.change_mode_S_and_UA)

    def init_ui(self):
        self.ui.p2_layout = QGridLayout(self.ui.page_2)
        self.ui.p2_layout.setHorizontalSpacing(5)
        self.ui.p2_layout.setVerticalSpacing(5)
        self.ui.p2_layout.addWidget(QLabel('<b>Inputs</b>'), 0, 0, 1, 1)
        self.add_widget_to_grid(self.ui.p2_layout, 1, 'p2_in_W', 'W, emitter width', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 2, 'p2_in_H', 'H, emitter height', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 3, 'p2_in_w', 'w, receiver location', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 4, 'p2_in_h', 'h, receiver location', 'm')
        self.add_widget_to_grid(self.ui.p2_layout, 5, 'p2_in_Q', 'Emitter heat flux', 'kW/m<sup>2</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 6, 'p2_in_Q_crit', 'Receiver critical heat flux', 'kW/m²')
        self.add_widget_to_grid(
            self.ui.p2_layout, 7, 'p2_in_half_S', '½S, emitter to boundary', 'm', descrip_cls='QRadioButton')
        self.add_widget_to_grid(
            self.ui.p2_layout, 8, 'p2_in_unprotected_area', 'Unprotected option', '%', descrip_cls='QRadioButton')
        self.ui.p2_layout.addWidget(QLabel('<b>Outputs</b>'), 9, 0, 1, 1)
        self.add_widget_to_grid(self.ui.p2_layout, 10, 'p2_out_Phi', 'Φ, configuration factor', '×10<sup>-3</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 11, 'p2_out_q', 'q, receiver heat flux', 'kW/m<sup>2</sup>')
        self.add_widget_to_grid(self.ui.p2_layout, 12, 'p2_out_S_or_UA', 'Allowable unprotected area', '%')

    def change_mode_S_and_UA(self):
        """update ui to align with whether to calculate boundary distance or unprotected area %"""

        # change input and output labels and units
        if self.ui.p2_in_half_S_label.isChecked():  # to calculate unprotected area percentage
            self.ui.p2_in_unprotected_area.setEnabled(False)  # disable UA related inputs
            self.ui.p2_in_unprotected_area_unit.setEnabled(False)  # disable UA related inputs
            self.ui.p2_in_half_S.setEnabled(True)  # enable S related inputs
            self.ui.p2_in_half_S_unit.setEnabled(True)  # enable S related inputs
            self.ui.p2_out_S_or_UA_label.setText('Allowable unprotected area')
            self.ui.p2_out_S_or_UA_unit.setText('%')
            self.ui.p2_out_S_or_UA.setToolTip('Solved maximum permitted unprotected area')
        elif self.ui.p2_in_unprotected_area_label.isChecked():  # to calculate separation to boundary
            self.ui.p2_in_half_S.setEnabled(False)  # disable S related inputs
            self.ui.p2_in_half_S_unit.setEnabled(False)  # disable S related inputs
            self.ui.p2_in_unprotected_area.setEnabled(True)  # enable UA related inputs
            self.ui.p2_in_unprotected_area_unit.setEnabled(True)  # enable UA related inputs
            self.ui.p2_out_S_or_UA_label.setText('½S, min. sep. distance')
            self.ui.p2_out_S_or_UA_unit.setText('m')
            self.ui.p2_out_S_or_UA.setToolTip('Solved minimum separation distance to boundary.')
        else:
            raise ValueError('Unknown value for input UA or S.')

        # clear outputs
        self.ui.p2_out_Phi.setText('')
        self.ui.p2_out_q.setText('')
        self.ui.p2_out_S_or_UA.setText('')

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
        def str2float(v_: str):
            try:
                return float(v_)
            except ValueError:
                return None

        # parse input parameters from ui
        W = str2float(self.ui.p2_in_W.text())
        H = str2float(self.ui.p2_in_H.text())
        w = str2float(self.ui.p2_in_w.text())
        h = str2float(self.ui.p2_in_h.text())
        if self.ui.p2_in_half_S_label.isChecked():
            S = str2float(self.ui.p2_in_half_S.text())
            if S:
                # convert surface to relevant boundary to surface to surface distance
                S *= 2.
        elif self.ui.p2_in_unprotected_area_label.isChecked():
            UA = str2float(self.ui.p2_in_unprotected_area.text())
            if UA is not None:
                # convert % to absolute i.e. 98% -> 0.98
                UA /= 100.
            else:
                raise ValueError('Unknown format, unprotected area input parameter should be a positive float')

        Q = str2float(self.ui.p2_in_Q.text())
        Q_a = str2float(self.ui.p2_in_Q_crit.text())

        # validate input values
        self.validate(W, 'unsigned float', 'Emitter width should be greater than 0')
        self.validate(H, 'unsigned float', 'Emitter height should be greater than 0')
        self.validate(w, float, 'Receiver offset "w" should be a number')
        self.validate(h, float, 'Receiver offset "h" should be a number')
        if UA is not None:
            try:
                assert all((UA > 0, UA <= 1))
            except AssertionError:
                raise ValueError('Unprotected area should be greater than 0 and less than 100 %')

        self.validate(Q_a, 'unsigned float', 'Receiver critical heat flux should be greater than 0')
        self.validate(Q, 'unsigned float', 'Emitter heat flux should be greater than 0')

        # check if enough inputs are provided for any calculation options
        try:
            assert all(i is not None for i in (W, H, w, h))

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

        self.ui.p2_out_Phi.setText(f'{phi * 1000:.2f}')
        self.ui.p2_out_q.setText(f'{q:.2f}')

        if S:
            self.ui.p2_out_S_or_UA.setText(f'{S / 2:.2f}')
        elif UA:
            self.ui.p2_out_S_or_UA.setText(f'{UA * 100:.2f}')

    def calculate(self):

        # clear ui output fields
        self.ui.p2_out_S_or_UA.clear()
        self.ui.p2_out_Phi.clear()
        self.ui.p2_out_q.clear()

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


if __name__ == "__main__":
    import sys
    from PySide2 import QtWidgets

    qapp = QtWidgets.QApplication(sys.argv)
    app = BR187SimpleBaseClass()
    app.show()
    qapp.exec_()
