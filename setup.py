#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=6.0", "htimeseries"]

setup_requirements = []

test_requirements = []

setup(
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
