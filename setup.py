# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from catstalk import __version__

setup(
    name="catstalk",
    version=__version__,
    description="Just an another static blog generator",
    long_description=open("README.md").read(),
    keywords="catstalk, blog, static",
    author="helloqiu",
    author_email="helloqiu95@gmail.com",
    url="https://github.com/helloqiu/Catstalk",
    packages=find_packages(),
    packages_data={"catstalk": ["resource/*"]},
    entry_points={
        "console_scripts": ["catstalk=catstalk.cli:parse"],
    },
    include_package_data=True,
    install_requires=open("requirements.txt").readlines(),
    license="MIT License",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python"
    ],
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=[
        "pytest",
    ],
)
