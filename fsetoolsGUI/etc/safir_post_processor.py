import re

import numpy as np


def out2pstrain(fp_out: str, fp_out_p1):
    count = 0
    f_out_p1 = open(fp_out_p1, 'w+')
    with open(fp_out, 'r') as f:
        while True:
            l = f.readline()
            if l:
                if 'strain' in l or 'TIME' in l:
                    f_out_p1.write(l)
                count += 1

                if count % 10000 == 0:
                    print(count, end='\r', flush=True)
            else:
                break
    f_out_p1.close()


def pstrain2dict(fp: str) -> dict:
    rp_time_str = re.compile(r'TIME[ ]*=[ ]+[0-9.0-9]+')
    rp_time_val = re.compile(r'[0-9.0-9]+')
    rp_shell_str = re.compile(r'SHELL\:[ ]*[0-9]+')
    rp_shell_val = re.compile(r'[0-9]+')
    rp_surf_str = re.compile(r'SURF\:[ ]*[0-9]+')
    rp_surf_val = re.compile(r'[0-9]+')
    rp_rebar_str = re.compile(r'REBAR\:[ ]*[0-9]+')
    rp_rebar_val = re.compile(r'[0-9]+')
    rp_strain_str = re.compile(r'Total strain[ ]*\:[ ]*[0-9\.]+')
    rp_strain_val = re.compile(r'[0-9\.]+')
    rp_strain_str2 = re.compile(r'Stress related strain[ ]*\:[ ]*[0-9\.]+')
    rp_strain_val2 = re.compile(r'[0-9\.]+')

    def get_value(s, rp1, rp2):
        s1 = rp1.findall(s)
        if s1:
            return float(rp2.findall(s1[0])[0])
        else:
            return None

    count = 0
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
                elif time_current:
                    list_time.append(time_current)
                    list_shell.append(get_value(l, rp_shell_str, rp_shell_val))
                    list_surf.append(get_value(l, rp_surf_str, rp_surf_val))
                    list_rebar.append(get_value(l, rp_rebar_str, rp_rebar_val))
                    list_strain.append(get_value(l, rp_strain_str, rp_strain_val))
                    list_strain2.append(get_value(l, rp_strain_str2, rp_strain_val2))

                count += 1

    return dict(
        list_time=np.asarray(list_time),
        list_shell=np.asarray(list_shell, dtype=int),
        list_surf=np.asarray(list_surf, dtype=int),
        list_rebar=np.asarray(list_rebar, dtype=int),
        list_strain=np.asarray(list_strain, dtype=float),
        list_strain2=np.asarray(list_strain2, dtype=float),
    )


def save_csv(fp: str, list_time, list_shell, list_surf, list_rebar, list_strain, list_strain2):
    data = zip(list_time, list_shell, list_surf, list_rebar, list_strain, list_strain2)
    data_list = [[j for j in i] for i in data]
    data_arr = np.array(data_list, dtype=float)
    np.savetxt(fp, data_arr, delimiter=",",
               header='time,shell,surf,rebar,strain,stress strain',
               fmt=['%10d', '%10d', '%10d', '%10d', '%10.7f', '%10.7f'])


def make_strain_lines_for_given_shell(unique_shell: int, list_time, list_shell, list_surf, list_rebar, list_strain,
                                      list_strain2):
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
                list_lines.append(dict(
                    x=time_,
                    y=strain_,
                    label=label_
                ))

    return list_lines
