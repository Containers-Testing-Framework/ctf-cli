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
        self.parser = argparse.ArgumentParser(
            description='CLI for running Containers Testing Framework')
        self.subparsers = self.parser.add_subparsers(dest="cli_action")
        self.add_args()
        self.add_remote_subparser()
        self.add_init_subparser()
        self.add_run_subparser()
        self.add_update_subparser()
        self.args = self.parser.parse_args(args)

    def add_remote_add_subparser(self, subparser):
        subparser.add_argument(
            dest='remote_type',
            choices=['steps', 'features'])

        subparser.add_argument(
            dest='url',
            help='module url')

        subparser.add_argument(
            "--project",
            dest='project',
            help="name of test project")

    def add_remote_remove_subparser(self, subparser):
        subparser.add_argument(
            dest='name')

    def add_remote_subparser(self):
        remote_subparser = self.subparsers.add_parser(
            'remote', help='addidng/removing test suites')
        remote_oper_subparser = remote_subparser.add_subparsers(
            dest='remote_action')
        self.add_remote_add_subparser(remote_oper_subparser.add_parser(
            'add', help='add remote repository'))
        self.add_remote_remove_subparser(remote_oper_subparser.add_parser(
            'remove', help='remove remote repository'))
        remote_oper_subparser.add_parser('list', help='list remote repositories')

    def add_run_subparser(self):
        run_subparser = self.subparsers.add_parser(
            'run', help="run test suite - default")
        run_subparser.add_argument(
            "-c",
            "--cli-config",
            default=None,
            dest='cli_config_path',
            help="Path to CLI configuration file" +
                 "(By default use only CLI arguments and default values)"
        )
        run_subparser.add_argument(
            "-t",
            "--tests-config",
            default=None,
            dest='tests_config_path',
            help="Path to tests configuration file. By default it will be searched for in test/ dir"
        )
        run_subparser.add_argument(
            "-d",
            "--behave-data",
            action='append',
            default=None,
            dest='behave_data',
            help="A way to set behave userdata"
        )
        run_subparser.add_argument(
            "-b",
            "--behave-tags",
            action='append',
            default=None,
            dest='behave_tags',
            help="A way to set behave test tags"
        )
        run_subparser.add_argument(
            "-j",
            "--junit",
            default=None,
            dest='junit',
            help="Junit folder to store results. If not passed junit reports will not be generated"
        )

    def add_update_subparser(self):
        self.subparsers.add_parser('update', help="update suites")

    def add_init_subparser(self):
        self.subparsers.add_parser('init', help="update suites")

    def add_args(self):
        self.parser.add_argument(
            "-v",
            "--verbose",
            default=False,
            action="store_true",
            help="Output is more verbose (recommended)"
        )

    def __getattr__(self, name):
        try:
            return getattr(self.args, name)
        except AttributeError:
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                return None
