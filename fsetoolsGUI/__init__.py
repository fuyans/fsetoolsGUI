import datetime
import os
import logging

c_handler = logging.StreamHandler()
c_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
)
logger = logging.getLogger('gui')
logger.setLevel(logging.INFO)
logger.addHandler(c_handler)

# make root directory of this app which will be used 1. when running the app; 2. pyinstaller at compiling the app.
if os.path.exists(os.path.dirname(__file__)):
    # this path should be used when running the app as a Python package (non compiled) and/or pyinstaller at compiling
    # stage.
    __root_dir__ = os.path.dirname(__file__)
elif os.path.exists(os.path.dirname(os.path.dirname(__file__))):
    # the path will become invalid when the app run after compiled as the dirname `fsetoolsGUI` will disappear.
    # instead, the parent folder of the project dir will be used.
    __root_dir__ = os.path.dirname(os.path.dirname(__file__))
else:
    __root_dir__ = None


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


__version__ = "0.0.5"
__date_released__ = datetime.datetime(2020, 8, 17)
__expiry_period_days__ = 360 + 180
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
