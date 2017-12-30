"""
A setuptools based setup module.

See:
 - https://packaging.python.org/en/latest/distributing.html
 - https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

setup(
    name="h800",
    version="0.8",
    description="H-800 Tools",
    url="https://github.com/jimlawton/h800",
    author="Jim Lawton",
    author_email="jim.lawton@gmail.com",
    license="GPL v2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux"
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[]
)
