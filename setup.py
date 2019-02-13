#!/usr/bin/env python

# Running setup.py requires having installed numpy and Cython. There are some
# complicated solutions that might make it possible to somehow add them to
# "setup_requirements" etc., but I decided they aren't worth it. We'd better wait until
# Python has better packaging tools (this shouldn't need more than 100 more years).
# More information on the complicated solutions:
# https://stackoverflow.com/questions/37471313/
# https://stackoverflow.com/questions/14657375/
# https://stackoverflow.com/questions/2379898/

import numpy
from setuptools import find_packages, setup
from Cython.Build import cythonize

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=6.0", "htimeseries"]

setup_requirements = ["cython>=0.29,<0.30"]

test_requirements = []

setup(
    ext_modules=cythonize("haggregate/regularize.pyx"),
    include_dirs=[numpy.get_include()],
    author="Antonis Christofides",
    author_email="antonis@antonischristofides.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    description="Aggregates htimeseries to larger steps",
    entry_points={"console_scripts": ["haggregate=haggregate.cli:main"]},
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="haggregate",
    name="haggregate",
    packages=find_packages(include=["haggregate"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/openmeteo/haggregate",
    version="0.1.0.dev0",
    zip_safe=False,
)
