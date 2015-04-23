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

from ctf_cli.logger import logger
from ctf_cli.config import CTFCliConfig
from ctf_cli.behave import BehaveWorkingDirectory, BehaveRunner

import os


class Application(object):

    def __init__(self, cli_args=None):
        """
        The Application implementation.
        """
        self._cli_conf = CTFCliConfig(cli_args)
        self._dockerfile = None
        self._image = None
        self._execution_dir_path = os.getcwd()
        self._working_dir_path = os.path.join(self._execution_dir_path,
                                              '{0}-behave-working-dir'.format(os.path.basename(self._execution_dir_path)))
        self._working_dir = None
        self._behave_runner = None

    def run(self):
        """
        The main application execution method
        """
        logger.debug("Running Containers Testing Framework cli")

        self._working_dir = BehaveWorkingDirectory(self._working_dir_path,
                                                   self._cli_conf.get(CTFCliConfig.GLOBAL_SECTION_NAME,
                                                                      CTFCliConfig.CONFIG_TESTS_CONFIG_PATH))
        # Setup Behave structure inside working directory
        # Clone common Features and steps into the working dir
        # Add the project specific Features and steps
        # Prepare the steps.py in the Steps dir that combines all the other
        self._working_dir.setup()

        # TODO: look for dockerfile if not passed

        # Execute Behave
        self._behave_runner = BehaveRunner(self._working_dir, self._cli_conf)
        return self._behave_runner.run()
