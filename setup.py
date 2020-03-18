#!/usr/bin/env python

import os
from codecs import open  # To use a consistent encoding

import setuptools

import fsetoolsGUI

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")) as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="fsetoolsGUI",
    version=fsetoolsGUI.__version__,
    description="Fire Safety Engineering Tools",
    author="Ian Fu",
    author_email=''.join([chr(ord(v)+i) for i, v in enumerate(r'ftw^jn:`eX_a"Va^')]),
    url="https://github.com/fsepy/fsetools",
    download_url="https://github.com/fsepy/fsetools/archive/master.zip",
    keywords=["fire", "safety", "engineering"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "fsetoolsGUI",
        "fsetoolsGUI.cli",
        "fsetoolsGUI.etc",
        "fsetoolsGUI.gui",
        "fsetoolsGUI.gui.layout",
        "fsetoolsGUI.gui.logic",
    ],
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["fsetoolsGUI=fsetoolsGUI.cli.__main__:main"]},
    ext_modules=[
        setuptools.extension.Extension("fputs", ["fsetoolsGUI/etc/realpythonexample.c"]),
        setuptools.extension.Extension("superfastexample", ["fsetoolsGUI/etc/msexample.cpp"])
    ],
)
