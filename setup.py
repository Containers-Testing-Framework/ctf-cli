#!/usr/bin/python

from setuptools import setup, find_packages

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
    long_description = "Containers Testing Framework (CTF) is a simple wrapper around Behave testing framework. Behave is a promising approach for testing containers, since it enables one to focus on describing the behavior of the container from a High Level and in simple English. For more information on how to use Behave and how to write tests using Behave, please refer to the Behave project page.",
    entry_points = {
        'console_scripts': ['ctf-cli=ctf_cli.cli_runner:run'],
    },
    install_requires=requirements
)
