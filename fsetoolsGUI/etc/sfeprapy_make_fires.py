import os
from os.path import join

import numpy as np
import pandas as pd
from sfeprapy.mcs0.mcs0_calc import evaluate_fire_temperature


def mcs0_make_fires(fp_mcs_input: str, fp_mcs_output_dir: str, index: int, case_name: str):
    # ===============
    # load input data
    # ===============
    df_mcs_inputs = pd.read_excel(fp_mcs_input, index_col=0)

    # ================
    # load output data
    # ================
    fp_csvs = [join(root, f) for root, dirs, files in os.walk(fp_mcs_output_dir) for f in files if f.endswith('.csv')]
    df_mcs_outputs: pd.DataFrame = pd.concat([pd.read_csv(fp) for fp in fp_csvs])
    df_mcs_outputs = df_mcs_outputs.loc[:, ~df_mcs_outputs.columns.str.contains('^Unnamed')]  # remove potential index column
    df_mcs_outputs.dropna(subset=['solver_time_equivalence_solved'], inplace=True)  # get rid of iterations without convergence for time equivalence

    kwargs: dict = df_mcs_inputs[case_name].to_dict()

    # remove stochastic parameters
    for key in list(kwargs.keys()):
        if ':' in key:
            kwargs.pop(key)

    kwargs_deterministic: dict = df_mcs_outputs.loc[(df_mcs_outputs['index'] == index) & (df_mcs_outputs['case_name'] == case_name)].to_dict(orient='list')
    assert all([len(i) == 1 for i in kwargs_deterministic.values()])
    kwargs_deterministic = {k: v[0] for k, v in kwargs_deterministic.items()}

    fire_time = np.arange(0, kwargs['fire_time_duration'] + kwargs['fire_time_step'], kwargs['fire_time_step'])

    kwargs.update(kwargs_deterministic)
    kwargs['fire_time'] = fire_time

    temperature = evaluate_fire_temperature(**kwargs)['fire_temperature']

    return dict(time=fire_time, temperature=temperature)


if __name__ == '__main__':
    mcs0_make_fires(
        fp_mcs_input='/Users/ian/Desktop/sfeprapy_test/test.xlsx',
        fp_mcs_output_dir='/Users/ian/Desktop/sfeprapy_test/mcs.out',
        index=100,
        case_name='Standard Case 1',
    )
