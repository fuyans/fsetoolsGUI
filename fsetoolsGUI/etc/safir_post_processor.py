import multiprocessing as mp
import os
import re
import subprocess
import time
from os import path
from typing import List, Dict, Callable

import numpy as np


def safir_batch_run_worker(args: List) -> List:
    def worker(
            cmd: str,
            cwd: str,
            fp_stdout: str = None,
            timeout_seconds: int = 1 * 60,
    ) -> List:
        try:
            if fp_stdout:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(fp_stdout, 'w+'))
            else:
                subprocess.call(cmd, cwd=cwd, timeout=timeout_seconds, stdout=open(os.devnull, 'w'))
            return [cmd, 'Success']
        except subprocess.TimeoutExpired:
            return [cmd, 'Timed out']

    kwargs, q = args
    result = worker(**kwargs)
    q.put(1)
    return result


def safir_batch_run(
        list_kwargs_in: List[Dict],
        func_mp: Callable = safir_batch_run_worker,
        n_proc: int = 1,
        dir_work: str = None,
        qt_progress_signal=None
):
    # ------------------------------------------
    # prepare variables used for multiprocessing
    # ------------------------------------------
    m, p = mp.Manager(), mp.Pool(n_proc, maxtasksperchild=1000)
    q = m.Queue()
    jobs = p.map_async(func_mp, [(dict_, q) for dict_ in list_kwargs_in])
    n_simulations = len(list_kwargs_in)

    # ---------------------
    # multiprocessing start
    # ---------------------
    while True:
        if jobs.ready():
            if qt_progress_signal:
                qt_progress_signal.emit(100)
            break  # complete
        else:
            if qt_progress_signal:
                qt_progress_signal.emit(int(q.qsize() / n_simulations * 100))
            time.sleep(1)  # in progress

    # --------------------------------------------
    # pull results and close multiprocess pipeline
    # --------------------------------------------
    p.close()
    p.join()
    mp_out = jobs.get()
    time.sleep(0.5)

    # ----------------------
    # save and print summary
    # ----------------------
    if dir_work:
        out = mp_out
        len_1 = int(max([len(' '.join(i[0])) for i in out]))
        summary = '\n'.join([f'{" ".join(i[0]):<{len_1}} - {i[1]:<{len_1}}' for i in out])
        print(summary)
        with open(os.path.join(dir_work, 'summary.txt'), 'w+') as f:
            f.write(summary)

    return mp_out


def out2pstrain(fp_out: str, fp_out_strain):
    """Convert Safir *.out file to a processed output file `fp_out_strain` containing strain data only."""
    count = 0
    with open(fp_out, 'r') as f, open(fp_out_strain, 'w+') as f_out_p1:
        while True:
            l = f.readline()
            if l:
                if 'strain' in l.lower() or 'time' in l.lower():
                    f_out_p1.write(l)
                count += 1

                if count % 10000 == 0:
                    print(count, end='\r', flush=True)
            else:
                break


def pstrain2dict(fp: str) -> dict:
    """Extract strain data from Safir *.out or processed output file containing strain data only and store in a dict.
    The resulting dict data structure:
    {
        list_time: [...],
        list_shell: [...],
        list_surf: [...],
        list_rebar: [...],
        list_strain: [...],
        list_strain2: [...],
    }
    All elements in the dict have the same length.
    """
    rp_time_str = re.compile(r'TIME[ ]*=[ ]+[0-9.0-9]+')
    rp_time_val = re.compile(r'[0-9.0-9]+')
    rp_shell_str = re.compile(r'SHELL:[ ]*[0-9]+')
    rp_shell_val = re.compile(r'[0-9]+')
    rp_surf_str = re.compile(r'SURF:[ ]*[0-9]+')
    rp_surf_val = re.compile(r'[0-9]+')
    rp_rebar_str = re.compile(r'REBAR:[ ]*[0-9]+')
    rp_rebar_val = re.compile(r'[0-9]+')
    rp_strain_str = re.compile(r'Total strain[ ]*:[ ]*[-0-9.]+|Strain[ ]*:[ ]*[-0-9.]+')
    rp_strain_val = re.compile(r'[-0-9.]+')
    rp_strain_str2 = re.compile(r'Stress related strain[ ]*:[ -]*[0-9.]+')
    rp_strain_val2 = re.compile(r'[-0-9.]+')

    def get_value(s, rp1, rp2):
        s1 = rp1.findall(s)
        if s1:
            return float(rp2.findall(s1[0])[0])
        else:
            return None

    time_current = 0
    list_time, list_shell, list_surf, list_rebar, list_strain, list_strain2 = [], [], [], [], [], []
    with open(fp, 'r') as f:
        while True:
            l = f.readline()
            if not l:
                break
            else:
                time = get_value(l, rp_time_str, rp_time_val)
                if time:
                    time_current = time
                elif time_current and 'SHELL' in l:
                    list_time.append(time_current)
                    list_shell.append(get_value(l, rp_shell_str, rp_shell_val))
                    list_surf.append(get_value(l, rp_surf_str, rp_surf_val))
                    list_rebar.append(get_value(l, rp_rebar_str, rp_rebar_val))
                    list_strain.append(get_value(l, rp_strain_str, rp_strain_val))
                    list_strain2.append(get_value(l, rp_strain_str2, rp_strain_val2))

    def list2arr(data: list, dtype):
        data = np.array(data)
        data[data is None] = -1
        return np.array(data, dtype=dtype)

    list_time = list2arr(list_time, float)
    list_shell = list2arr(list_shell, int)
    list_surf = list2arr(list_surf, int)
    list_rebar = list2arr(list_rebar, int)
    list_strain = list2arr(list_strain, float)
    list_strain2 = list2arr(list_strain2, float)

    return dict(
        list_time=list_time, list_shell=list_shell, list_surf=list_surf,
        list_rebar=list_rebar, list_strain=list_strain, list_strain2=list_strain2,
    )


def save_csv(fp: str, list_time, list_shell, list_surf, list_rebar, list_strain, list_strain2):
    data = zip(list_time, list_shell, list_surf, list_rebar, list_strain, list_strain2)
    data_list = [[j for j in i] for i in data]
    data_arr = np.array(data_list, dtype=float)
    np.savetxt(fp, data_arr, delimiter=",",
               header='time,shell,surf,rebar,strain,stress strain',
               fmt=['%10d', '%10d', '%10d', '%10d', '%10.7f', '%10.7f'])


def make_strain_lines_for_given_shell(
        unique_shell: int,
        list_time,
        list_shell,
        list_surf,
        list_rebar,
        list_strain,
        list_strain2
):
    """"""
    list_unique_surf = list(set(list_surf[list_shell == unique_shell]))
    list_unique_surf.sort()

    list_lines = []
    for unique_surf in list_unique_surf:
        list_unique_rebar = list(set(list_rebar[list_surf == unique_surf]))
        list_unique_rebar.sort()
        for unique_rebar in list_unique_rebar:
            time_ = list_time[
                (list_shell == unique_shell) & (list_surf == unique_surf) & (list_rebar == unique_rebar)
                ]
            strain_ = list_strain[
                (list_shell == unique_shell) & (list_surf == unique_surf) & (list_rebar == unique_rebar)
                ]
            label_ = f'surf {unique_surf:g} rebar {unique_rebar:g}'

            if len(strain_) > 0:
                list_lines.append(
                    dict(
                        x=time_,
                        y=strain_,
                        label=label_
                    )
                )

    return list_lines


def tor2tem(dir_work: str, fp_tor2temfix: str):
    # ----------
    # user input
    # ----------
    # dir_work = path.realpath(r'C:\Users\IanFu\Desktop\safir_ben_batch_8_200528\safir_ben_batch_8_200528')
    # fp_tor2temfix = path.realpath(r'C:\Program Files\GiD\GiD 14.1.0d\problemtypes\SAFIR2019\Safir_Thermal_2d.gid\TorToTemFix.exe')

    # --------------------------------------
    # prepare inputs, cmd, cwd and fp_stdout
    # --------------------------------------
    assert path.isdir(dir_work)
    list_fp = list()
    for root, dirs, files in os.walk(dir_work):
        for file_ in files:
            if file_.endswith('.in'):
                list_fp.append(root)
    list_fp = list(set(list_fp))

    for i in list_fp:
        try:
            subprocess.call([fp_tor2temfix, i])
            print(f'{i} - OK')
        except Exception as e:
            print(f'{i} - Failed')
