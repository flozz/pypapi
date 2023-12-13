#!/usr/bin/env python
# encoding: UTF-8

import os
import subprocess

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class CustomBuildPy(build_py):
    def run(self):
        os.environ["CFLAGS"] = "%s -fPIC -Werror=format-truncation=0" % os.environ.get(
            "CFLAGS", ""
        )
        subprocess.call("cd papi/src/ && ./configure", shell=True)  # noqa
        subprocess.call("cd papi/src/ && make", shell=True)  # noqa
        build_py.run(self)


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="python_papi",
    version="5.5.1.6",
    description="Python binding for the PAPI library",
    url="https://github.com/flozz/pypapi",
    project_urls={
        "Source Code": "https://github.com/flozz/pypapi",
        "Documentation": "https://flozz.github.io/pypapi/",
        "Changelog": "https://github.com/flozz/pypapi#changelog",
        "Issues": "https://github.com/flozz/pypapi/issues",
        "Chat": "https://discord.gg/P77sWhuSs4",
        "Donate": "https://github.com/flozz/pypapi#support-this-project",
    },
    license="WTFPL",
    long_description=long_description,
    keywords="papi perf performance",
    author="Fabien LOISON, Mathilde BOUTIGNY",
    # author_email="",
    packages=find_packages(),
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
            "sphinx",
            "sphinx-rtd-theme",
        ]
    },
    cffi_modules=["pypapi/papi_build.py:ffibuilder"],
    cmdclass={
        "build_py": CustomBuildPy,
    },
)
