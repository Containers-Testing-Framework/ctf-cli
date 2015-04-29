# -*- coding: utf-8 -*-
#
# Containers Testing Framework command line interface
# Copyright (C) 2015  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse


class ArgumentsParser(object):
    """ Class for processing data from commandline """

    def __init__(self, args=None):
        """ parse arguments """
        self.parser = argparse.ArgumentParser(description='CLI for running Containers Testing Framework')
        self.add_args()
        self.args = self.parser.parse_args(args)

    def add_args(self):
        self.parser.add_argument(
            "-v",
            "--verbose",
            default=False,
            action="store_true",
            help="Output is more verbose (recommended)"
        )
        self.parser.add_argument(
            "-c",
            "--cli-config",
            default=None,
            dest='cli_config_path',
            help="Path to CLI configuration file (By default use only CLI arguments and default values)"
        )
        self.parser.add_argument(
            "-t",
            "--tests-config",
            default=None,
            dest='tests_config_path',
            help="Path to tests configuration file. By default it will be searched for in test/ dir"
        )
        self.parser.add_argument(
            "-f",
            "--dockerfile",
            default=None,
            dest='dockerfile',
            help="Path to Dockerfile to use. If not passed, will be searched for in the current directory"
        )
        self.parser.add_argument(
            "-i",
            "--image",
            default=None,
            dest='image',
            help="Image to use for testing. If not passed, the image will be built from the Dockerfile."
        )
        self.parser.add_argument(
            "-j",
            "--junit",
            default=None,
            dest='junit',
            help="Junit folder to store results. If not passed junit reports will not be generated"
        )

    def __getattr__(self, name):
        try:
            return getattr(self.args, name)
        except AttributeError:
            return object.__getattribute__(self, name)
