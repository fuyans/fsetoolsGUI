import datetime
import os
from typing import Union


# make root directory of this app which will be used 1. when running the app; 2. pyinstaller at compiling the app.
__root_dir__ = None
if os.path.exists(os.path.dirname(__file__)):
    # this path should be used when running the app as a Python package (non compiled) and/or pyinstaller at compiling
    # stage.
    __root_dir__ = os.path.dirname(__file__)
elif os.path.exists(os.path.dirname(os.path.dirname(__file__))):
    # the path will become invalid when the app run after compiled as the dirname `fsetoolsGUI` will disappear.
    # instead, the parent folder of the project dir will be used.
    __root_dir__ = os.path.dirname(os.path.dirname(__file__))


class AppInfo:
    __data = {
        'code': {
            "short name": 'a short name to be used as button name etc',
            'long name': 'a long name to be used as window title, tip text etc',
            'doc file path': 'documentation file path, in html format, used in gui About dialog'
        },
        '0101': dict(
            short_name='ADB\ndata sheet\n1',
            long_name='ADB vol. 2 data sheet no. 1 - means of escape',
        ),
        '0102': dict(
            short_name='BS 9999\ndata sheet\n1',
            long_name='BS 9999 data sheet no. 1 - means of escape',
        ),
        '0103': dict(
            short_name='BS 9999\nmerging\nflow',
            long_name='BS 9999 merging flow at final exit level',
        ),
        '0104': dict(
            short_name='ADB\nmerging\nflow',
            long_name='ADB merging flow at final exit level',
        ),
        '0111': dict(
            short_name='PD 7974\nheat\ndetector\nactivation',
            long_name='PD 7974 heat detector device activation time calculator',
        ),
        '0401': dict(
            short_name='BR 187\nparallel',
            long_name='BR 187 parallel oriented rectangle emitter and receiver',
        ),
        '0402': dict(
            short_name='BR 187\nperp.',
            long_name='BR 187 perpendicular oriented rectangle emitter and receiver',
        ),
        '0403': dict(
            short_name='BR 187\nparallel\neccentric',
            long_name='BR 187 parallel oriented rectangle emitter and eccentric receiver',
        ),
        '0404': dict(
            short_name='BR 187\nperp.\neccentric',
            long_name='BR 187 perpendicular oriented rectangle emitter and eccentric receiver',
        ),
        '0405': dict(
            short_name='TRA\n3D single point',
            long_name='TRA 3D polygon emitter and a single point',
        ),
        '0406': dict(
            short_name='TRA\n2D\nparallel',
            long_name='TRA 2D parallel orientated contour plot',
        ),
        '0407': dict(
            short_name='TRA\ncuboid\nenclosure\nmodel',
            long_name='TRA cuboid enclosure model',
        ),
        '0601': dict(
            short_name='OFR\nfile naming\nconvention',
            long_name='OFR file name generator',
        ),
        '0602': dict(
            short_name='PD 7974\nflame height',
            long_name='PD 7974 flame height calculator',
        ),
        '0611': dict(
            short_name='EC 1991\nparametric\nfire',
            long_name='EC 1991-1-2 parametric fire generator',
        ),
        '0620': dict(
            short_name='Probability\ndistribution',
            long_name='Probability distribution',
        ),
    }

    def __init__(self, code: Union[int, str] = None):
        if isinstance(code, str):
            code = int(code)
        self.__code = f'{code:04d}'

    @property
    def long_name(self):
        try:
            return self.__data[str(self.__code)]['long_name']
        except KeyError:
            return None

    @property
    def short_name(self):
        try:
            return self.__data[str(self.__code)]['short_name']
        except KeyError:
            return None

    @property
    def short_and_long_names(self):
        try:
            return self.__data[str(self.__code)]['short_name'], self.__data[str(self.__code)]['long_name']
        except KeyError:
            return None

    @property
    def doc_file_path(self):
        return os.path.join(__root_dir__, 'gui', 'docs', f'{self.__code}.html')

    @property
    def doc_html(self):
        with open(self.doc_file_path, 'r') as f:
            return f.read()


"""
VERSION IDENTIFICATION RULES DOCUMENTED IN PEP 440.

Version scheme
==============

Distributions are identified by a public version identifier which supports all defined version comparison operations

The version scheme is used both to describe the distribution version provided by a particular distribution archive, as
well as to place constraints on the version of dependencies needed in order to build or run the software.

Public version identifiers
--------------------------

The canonical public version identifiers MUST comply with the following scheme:

`[N!]N(.N)*[{a|b|rc}N][.postN][.devN]`

Public version identifiers MUST NOT include leading or trailing whitespace.

Public version identifiers MUST be unique within a given distribution.

See also Appendix B : Parsing version strings with regular expressions which provides a regular expression to check
strict conformance with the canonical format, as well as a more permissive regular expression accepting inputs that may
require subsequent normalization.

Public version identifiers are separated into up to five segments:

    - Epoch segment: N!
    - Release segment: N(.N)*
    - Pre-release segment: {a|b|rc}N
    - Post-release segment: .postN
    - Development release segment: .devN

"""


__version__ = "0.0.4"
__date_released__ = datetime.datetime(2020, 4, 14)
__expiry_period_days__ = 180
__remote_version_url__ = r'hsrmo5)(jXw-efpco[mjeqaljo_gl%cnk,bpsZfj/ucoodigk&m`qqam)_k\tnmioBOBWFFQ,gojh'

if __name__ == "__main__":
    import re

    def is_canonical(version):
        return (
                re.match(
                    r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
                    version,
                )
                is not None
        )

    assert is_canonical(__version__)
