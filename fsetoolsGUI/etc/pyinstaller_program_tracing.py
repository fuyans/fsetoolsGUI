import os
import sys
from contextlib import suppress

pid = os.getpid()


def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    elif event == 'return':
        print('[{}] {} => {}'.format(pid, func_name, arg))
        return
    line_no = frame.f_lineno
    filename = co.co_filename

    c_frame = frame
    c_filename = filename
    c_line_no = line_no

    with suppress(Exception):
        for i in range(10):
            if not (c_line_no == line_no and c_filename == filename):
                break

            c_frame = frame.f_back
            c_line_no = c_frame.f_lineno
            c_filename = c_frame.f_code.co_filename
        else:
            c_line_no = 'UNKNOWN'
            c_filename = 'UNKNOWN'

    if 'multiprocessing' not in filename:
        return

    # with suppress(Exception):
    print('[{}] Call to {} on line {} of {} from {} of {}'.format(pid, func_name, line_no, filename, c_line_no, c_filename))

    for i in range(frame.f_code.co_argcount):
        #    with suppress(Exception):
        name = frame.f_code.co_varnames[i]
        if name in frame.f_locals:
            value = frame.f_locals[name]
        elif name in frame.f_globals:
            value = frame.f_globals[name]
        else:
            value = ''

        if type(value) is not str:
            with suppress(Exception):
                value = repr(value)

        if type(value) is not str:
            with suppress(Exception):
                value = str(value)

        if type(value) is not str:
            value = ''

        print("[{}]    Argument {} is {}".format(pid, name, value))


sys.settrace(trace_calls)