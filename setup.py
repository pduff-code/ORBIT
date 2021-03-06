""""Distribution setup"""

import os

from setuptools import setup, find_packages

import versioneer

ROOT = os.path.abspath(os.path.dirname(__file__))

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="ORBIT",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Offshore Renewables Balance of system and Installation Tool",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    install_requires=[
        "numpy",
        "matplotlib",
        "simpy",
        "marmot-agents>=0.2.5",
        "scipy",
        "pandas",
        "pyyaml",
        "geopy",
        "openmdao>= 2.0",
    ],
    extras_require={
        "dev": [
            "pre-commit",
            "pylint",
            "flake8",
            "black",
            "isort",
            "pytest",
            "pytest-cov",
            "sphinx",
            "sphinx-rtd-theme",
        ]
    },
    test_suite="pytest",
    tests_require=["pytest", "pytest-cov"],
)
