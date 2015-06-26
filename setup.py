#!/usr/bin/python

from setuptools import setup, find_packages
import codecs

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "ctf-cli",
    version = "0.0.1.dev0",
    packages = find_packages(exclude=["test"]),
    url = 'https://github.com/Containers-Testing-Framework/ctf-cli',
    download_url = "https://github.com/Containers-Testing-Framework/ctf-cli/archive/%s.tar.gz" % 'master',
    description = 'Simple command line tool for executing Containers Testing Framework',
    license='GPLv2',
    keywords = 'docker behave',
    long_description = codecs.open('README.rst', encoding="utf8").read(),
    entry_points = {
        'console_scripts': ['ctf-cli=ctf_cli.cli_runner:run'],
    },
    install_requires=requirements
)
