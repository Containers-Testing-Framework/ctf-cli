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

import os
import shutil
import sys
from subprocess import check_call, CalledProcessError

from ctf_cli.logger import logger
from ctf_cli.config import CTFCliConfig
from ctf_cli.behave import BehaveWorkingDirectory, BehaveRunner
from ctf_cli.exceptions import CTFCliError
from ctf_cli.common_environment import sample_ctl_ctf_config, common_steps_py_content


class Application(object):

    def __init__(self, cli_args=None):
        """
        The Application implementation.
        """
        self._execution_dir_path = os.getcwd()
        self._working_dir_path = os.path.join(self._execution_dir_path,
                                              'workdir')

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
        try:
            check_call('git rev-parse &> /dev/null', shell=True)
        except CalledProcessError:
            logger.info("Directory is not under git control, running git init")
            check_call("git init &> /dev/null", shell=True)

        # Create test dir if it is missing
        tests_dir = os.path.join(self._execution_dir_path, "tests")
        if os.path.exists(tests_dir):
            logger.info("Directory tests already exists")
        else:
            logger.info("Creating tests directory")
            os.mkdir(tests_dir)
            check_call("git add %s" % tests_dir, shell=True)

        features_dir = os.path.join(tests_dir, "features")
        if os.path.exists(features_dir):
            logger.info("Directory tests/features already exists")
        else:
            logger.info("Creating tests/features directory")
            os.mkdir(features_dir)
            check_call("git add %s" % features_dir, shell=True)

        steps_dir = os.path.join(tests_dir, "steps")
        if os.path.exists(steps_dir):
            logger.info("Directory tests/steps already exists")
        else:
            logger.info("Creating tests/steps directory")
            os.mkdir(steps_dir)
            check_call("git add %s" % steps_dir, shell=True)

        # TODO: check that this file is actually necessary
        steps_init_file = os.path.join(steps_dir, "__init__.py")
        if os.path.exists(steps_init_file):
            logger.info("File tests/steps/__init__.py already exists")
        else:
            logger.info("Creating tests/steps/__init__.py file")
            open(steps_init_file, "a").close()
            check_call("git add %s" % steps_init_file, shell=True)

        steps_py_file = os.path.join(steps_dir, "steps.py")
        if os.path.exists(steps_py_file):
            logger.info("File tests/steps/steps.py already exists")
        else:
            logger.info("Creating tests/steps/steps.py file")
            with open(steps_py_file, "w") as f:
                f.write(common_steps_py_content)
            check_call("git add %s" % steps_py_file, shell=True)

        # Copy sample configuration
        ctf_conf_file = os.path.join(self._execution_dir_path, "ctf.conf")
        if os.path.exists(ctf_conf_file):
            logger.info("File ctf.conf already exists")
        else:
            logger.info("Creating ctf.conf file")
            # Create environment.py
            with open(ctf_conf_file, "w") as f:
                f.write(sample_ctl_ctf_config)
            check_call("git add %s" % ctf_conf_file, shell=True)

    def add_remote(self):
        if 'feature' in self._cli_conf.get(
                CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_REMOTE_TYPE):
            self.add_remote_feature()
        else:
            self.add_remote_step()

    def add_remote_feature(self):
        project = self._cli_conf.get(
            CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_REMOTE_PROJECT)
        if project is None:
            path = "tests/features/"
        else:
            path = "tests/features/" + project
        self.add_submodule(path)

    def add_remote_step(self):
        project = self._cli_conf.get(
            CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_REMOTE_PROJECT)
        if project is None:
            path = "tests/steps/"
        else:
            path = "tests/steps/" + project
        self.add_submodule(path)

    def list_remotes(self):
        check_call("git submodule -q foreach 'git config --get remote.origin.url'", shell=True)

    def add_submodule(self, path):
        url = self._cli_conf.get(CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_REMOTE_URL)
        dirname = os.path.splitext(os.path.basename(url))[0].replace('-', '_')
        check_call('git submodule add %s %s' % (url, path + "/" + dirname), shell=True)

    def remove_remote(self):
        name = self._cli_conf.get(CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_REMOTE_NAME)
        check_call('git submodule deinit -f %s' % name, shell=True)
        check_call('git config -f .gitmodules --remove-section "submodule.%s"' % name, shell=True)
        gitmodules_dir = os.path.join(os.path.abspath(".git/modules"), name)
        shutil.rmtree(gitmodules_dir)
        shutil.rmtree(name)

    def run(self):
        """
        The main application execution method
        """
        logger.info("Running Containers Testing Framework cli")

        check_call("git submodule update --init", shell=True)

        # TODO: Remove this or rework, once more types are implemented
        if self._cli_conf.get(
                CTFCliConfig.GLOBAL_SECTION_NAME, CTFCliConfig.CONFIG_EXEC_TYPE) != 'ansible':
            raise CTFCliError("Wrong ExecType configured. Currently only 'ansible' is supported!")

        self._working_dir = BehaveWorkingDirectory(self._working_dir_path, self._cli_conf)

        # Setup Behave structure inside working directory
        # Clone common Features and steps into the working dir
        # Add the project specific Features and steps
        # Prepare the steps.py in the Steps dir that combines all the other
        self._working_dir.setup()

        # Execute Behave
        self._behave_runner = BehaveRunner(self._working_dir, self._cli_conf)
        sys.exit(self._behave_runner.run())

    def update(self):
        """
        Update app submodules
        """
        logger.info("Updating remote test and features")

        check_call("git submodule foreach git pull --rebase origin master", shell=True)
