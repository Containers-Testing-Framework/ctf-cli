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

from ctf_cli import settings


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
            "--config",
            default=settings.DEFAULT_CONFIG_LOCATION,
            dest='config_path',
            help="Path to configuration file (default: '{0}')".format(settings.DEFAULT_CONFIG_LOCATION)
        )

    def __getattr__(self, name):
        try:
            return getattr(self.args, name)
        except AttributeError:
            return object.__getattribute__(self, name)
