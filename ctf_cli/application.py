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
from ctf_cli.exceptions import CTFCliError
from ctf_cli.common_environment import common_environment_py_content, sample_ctl_ctf_config

import os
import shutil


class Application(object):

    def __init__(self, cli_args=None):
        """
        The Application implementation.
        """
        self._execution_dir_path = os.getcwd()
        self._working_dir_path = os.path.join(self._execution_dir_path,
                                              '{0}-behave-working-dir'.format(os.path.basename(self._execution_dir_path)))
        self._working_dir = None
        self._behave_runner = None

        if not cli_args.cli_config_path:
            cli_args.cli_config_path = CTFCliConfig.find_cli_config(self._execution_dir_path)
        self._cli_conf = CTFCliConfig(cli_args)

    def init(self):
        """
        Initialize default app test structure
        """
        logger.info("Initialize default directory structure")

        # Make sure we're in a directory under git control
        if not os.path.isdir(".git") or \
           os.system('git rev-parse 2> /dev/null > /dev/null') != 0:
            logger.info("Directory is not under git control, running git init")
            os.system("git init")

        # Create test dir if it is missing
        tests_dir = os.path.join(self._execution_dir_path, "tests")
        if os.path.exists(tests_dir):
            logger.info("Directory tests already exists")
        else:
            logger.info("Creating tests directory")
            os.mkdir(tests_dir)
            os.system("git add %s" % tests_dir)

        env_py_path = os.path.join(tests_dir, "environment.py")
        if os.path.exists(env_py_path):
            logger.info("File tests/environment.py already exists")
        else:
            logger.info("Creating environment.py")
            # Create environment.py
            with open(env_py_path, "w") as f:
                f.write(common_environment_py_content)
            os.system("git add %s" % env_py_path)

        features_dir = os.path.join(tests_dir, "features")
        if os.path.exists(features_dir):
            logger.info("Directory tests/features already exists")
        else:
            logger.info("Creating tests/features directory")
            os.mkdir(features_dir)
            os.system("git add %s" % features_dir)

        steps_dir = os.path.join(tests_dir, "steps")
        if os.path.exists(steps_dir):
            logger.info("Directory tests/steps already exists")
        else:
            logger.info("Creating tests/steps directory")
            os.mkdir(steps_dir)
            os.system("git add %s" % steps_dir)

        # TODO: check that this file is actually necessary
        steps_init_file = os.path.join(steps_dir, "__init__.py")
        if os.path.exists(steps_init_file):
            logger.info("File tests/steps/__init__.py already exists")
        else:
            logger.info("Creating tests/steps/__init__.py file")
            open(steps_init_file, "a").close()
            os.system("git add %s" % steps_init_file)

        # Add common-features and common-steps as submodules

        # TODO:  make this generic when a different type of container is specified
        common_features_dir = os.path.join(features_dir, "common-docker")
        if os.path.exists(common_features_dir):
            logger.info("Directory tests/features/common-docker already exists")
        else:
            logger.info("Adding tests/features/common-docker as a submodule")
            os.system('git submodule add https://github.com/Containers-Testing-Framework/common-features.git tests/features/common-features')

        common_steps_dir = os.path.join(steps_dir, "common_steps")
        if os.path.exists(common_steps_dir):
            logger.info("Directory tests/steps/common_steps already exists")
        else:
            logger.info("Adding tests/steps/common_steps as a submodule")
            os.system('git submodule add https://github.com/Containers-Testing-Framework/common-steps.git tests/steps/common_steps')

        # Copy sample configuration
        ctf_conf_file = os.path.join(self._execution_dir_path, "ctf.conf")
        if os.path.exists(ctf_conf_file):
            logger.info("File ctf.conf already exists")
        else:
            logger.info("Creating ctf.conf file")
            # Create environment.py
            with open(ctf_conf_file, "w") as f:
                f.write(sample_ctl_ctf_config)
            os.system("git add %s" % ctf_conf_file)

    def run(self):
        """
        The main application execution method
        """
        logger.info("Running Containers Testing Framework cli")

        # If no Dockerfile passed on the cli, try to use one from the execution directory
        if not self._cli_conf.get(CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_DOCKERFILE):
            local_file = os.path.join(self._execution_dir_path, 'Dockerfile')
            if not os.path.isfile(local_file):
                raise CTFCliError("No Dockerfile passed on the cli and no Dockerfile "
                                  "is present in the current directory!")
            logger.debug("Using Dockerfile from the current directory.")
            self._cli_conf.set(CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_DOCKERFILE, local_file)

        # TODO: Remove this or rework, once more types are implemented
        if self._cli_conf.get(CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_EXEC_TYPE) != 'ansible':
            raise CTFCliError("Wrong ExecType configured. Currently only 'ansible' is supported!")

        self._working_dir = BehaveWorkingDirectory(self._working_dir_path, self._cli_conf)

        # Setup Behave structure inside working directory
        # Clone common Features and steps into the working dir
        # Add the project specific Features and steps
        # Prepare the steps.py in the Steps dir that combines all the other
        self._working_dir.setup()

        # Execute Behave
        self._behave_runner = BehaveRunner(self._working_dir, self._cli_conf)
        return self._behave_runner.run()

    def update(self):
        """
        Update app submodules
        """
        pass