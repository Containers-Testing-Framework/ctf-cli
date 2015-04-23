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
import glob
from subprocess import check_call, call, CalledProcessError
from six.moves.configparser import ConfigParser

from ctf_cli.logger import logger
from ctf_cli.exceptions import CTFCliError
from ctf_cli.config import CTFCliConfig


class BehaveTestsConfig(object):
    """
    Configuration parser for tests configuration
    """
    STEPS_OPTION = 'Steps'
    FEATURES_OPTION = "Features"

    def __init__(self, conf_path):
        self._config = ConfigParser()
        self._config_path = conf_path

        try:
            self._config.read(self._config_path)[0]
        except IndexError:
            logger.warning("Tests configuration '%s' can not be read!")
        else:
            logger.debug("Using Tests configuration from '%s'.")

    def __getattr__(self, name):
        """
        Forward all ConfigParser attributes to ConfigParser object

        :param name: name of the attribute
        :return: returns the selected attribute
        """
        try:
            return getattr(self._config, name)
        except AttributeError:
            return object.__getattribute__(self, name)

    def get_tests(self):
        return self._config.sections()

    def get_test_steps(self, test_name):
        return self._config.get(test_name, self.STEPS_OPTION)

    def get_test_features(self, test_name):
        return self._config.get(test_name, self.FEATURES_OPTION)


class BehaveWorkingDirectory(object):
    """
    Class representing the Behave working directory
    """

    def __init__(self, working_dir, tests_conf_path=None):
        self._working_dir = working_dir
        self._execution_dir = os.path.dirname(self._working_dir)

        if os.path.isdir(os.path.join(self._execution_dir, 'test')):
            self._project_tests_dir = os.path.join(self._execution_dir, 'test')
        elif os.path.isdir(os.path.join(self._execution_dir, 'tests')):
            self._project_tests_dir = os.path.join(self._execution_dir, 'tests')
        else:
            # Use the execution dir if we don't have any better option
            self._project_tests_dir = self._execution_dir

        self._features_dir = os.path.join(self._working_dir, 'features')
        self._steps_dir = os.path.join(self._working_dir, 'steps')

        if tests_conf_path is None:
            self._tests_conf_path = self.find_tests_config(self._project_tests_dir)
        else:
            self._tests_conf_path = tests_conf_path
        if self._tests_conf_path is not None:
            self._tests_conf = BehaveTestsConfig(self._tests_conf_path)
        else:
            self._tests_conf = None

    def path(self):
        return self._working_dir

    def setup(self):
        """
        Setup the working directory

        :return:
        """
        self._check_working_dir()
        self._setup_dir_structure()
        self._add_project_specific_features()
        self._add_project_specific_steps()
        self._add_project_specific_environment_py()
        if self._tests_conf:
            self._add_remote_features()
            self._add_remote_steps()
        self._combine_steps()

    @staticmethod
    def find_tests_config(tests_path):
        """
        Find a tests config in the tests directory

        :param tests_path: path to tests/ directory containing Features and Steps
        :return: path to a config file or None if not found
        """
        logger.debug("Looking for tests configuration inside '%s'", tests_path)
        f = glob.glob(os.path.join(tests_path, 'test*.ini'))
        logger.debug(str(f))
        if not f:
            f = glob.glob(os.path.join(tests_path, 'test*.conf'))
            logger.debug(str(f))

        if not f:
            logger.debug("Didn't find any tests configuration file!")
            return None
        else:
            logger.debug("Found configuration file: %s", str(f))
            return os.path.join(tests_path, f[0])

    def _check_working_dir(self):
        """
        Check if working directory exists. Remove it if it exists and then recreate. Create it if it does not exist
        """
        if os.path.exists(self._working_dir):
            logger.debug("Working directory '%s' exists. Removing it!", self._working_dir)
            shutil.rmtree(self._working_dir)

        logger.debug("Creating working directory '%s'.", self._working_dir)
        os.mkdir(self._working_dir)

    def _setup_dir_structure(self):
        """
        Create directory structure and create git repo where appropriate
        :return:
        """
        logger.debug("Setting up Behave working directory")

        for d in (self._features_dir, self._steps_dir):
            os.mkdir(d)

    def _add_project_specific_steps(self):
        """
        Adds project specific steps from execution_dir/test/steps into the
        steps in working directory.

        :return:
        """
        project_steps_dir = os.path.join(self._project_tests_dir, 'steps')
        if os.path.exists(project_steps_dir):
            logger.info("Using project specific steps from '%s'", project_steps_dir)
            shutil.copytree(project_steps_dir, os.path.join(self._steps_dir,
                                                       '{0}_steps'.format(os.path.basename(
                                                           self._execution_dir).replace('-', '_'))))

        else:
            logger.warning("Not using project specific steps. '%s' does not exist!", project_steps_dir)

    def _add_project_specific_features(self):
        """
        Adds project specific features from execution_dir/test/features into the
        features in working directory

        :return:
        """
        project_features_dir = os.path.join(self._project_tests_dir, 'features')
        if os.path.exists(project_features_dir):
            logger.info("Using project specific features from '%s'", project_features_dir)
            shutil.copytree(project_features_dir, os.path.join(self._features_dir,
                                                          '{0}_features'.format(os.path.basename(
                                                              self._execution_dir).replace('-', '_'))))
        else:
            logger.warning("Not using project specific features. '%s' does not exist!", project_features_dir)

    def _add_project_specific_environment_py(self):
        """
        Adds project specific environment.py from execution_dir/test/ into the
        working directory

        :return:
        """
        project_environment_py = os.path.join(self._project_tests_dir, 'environment.py')
        if os.path.exists(project_environment_py):
            logger.info("Using project specific environment.py from '%s'", project_environment_py)
            shutil.copy(project_environment_py, self._working_dir)
        else:
            logger.warning("Not using project specific environment.py. '%s' does not exist!", project_environment_py)

    def _add_remote_steps(self):
        """
        Add all remote steps
        :return:
        """
        for test in self._tests_conf.get_tests():
            remote_repo = self._tests_conf.get_test_steps(test)
            local_dir = os.path.join(self._steps_dir, '{0}_steps'.format(test).replace('-', '_'))
            logger.debug("Cloning remote test Steps from '%s' to '%s'", remote_repo, local_dir)
            try:
                check_call(['git', 'clone', remote_repo, local_dir])
            except CalledProcessError as e:
                raise CTFCliError("Cloning of {0} failed!\n{1}".format(remote_repo, str(e)))

    def _add_remote_features(self):
        """
        Add all remote features
        :return:
        """
        for test in self._tests_conf.get_tests():
            remote_repo = self._tests_conf.get_test_features(test)
            local_dir = os.path.join(self._features_dir, '{0}_features'.format(test).replace('-', '_'))
            logger.debug("Cloning remote test Features from '%s' to '%s'", remote_repo, local_dir)
            try:
                check_call(['git', 'clone', remote_repo, local_dir])
            except CalledProcessError as e:
                raise CTFCliError("Cloning of {0} failed!\n{1}".format(remote_repo, str(e)))

    @staticmethod
    def get_import_statements(path):
        """
        Generate import statements

        :param path: path to dir from which to generate import statements
        :return: list of strings containing import statement
        """
        imports = []

        for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True):
            module = dirpath.replace(path, '').strip(os.sep).replace(os.sep, '.')
            # generate imports for the *.py files in the current dir

            # skip hidden directories and their subdirs
            dirs = [x for x in dirpath.replace(path, '').split(os.sep) if x.startswith('.')]
            if dirs:
                logger.debug("Skipping, since dirpath '%s' contains hidden dir: %s", dirpath, str(dirs))
                continue

            for f in filenames:
                # skip NON Python files
                if not f.endswith('.py'):
                    continue
                if f == '__init__.py':
                    continue

                logger.debug("Adding import for '%s'", os.path.join(dirpath, f))
                imports.append('from {0}.{1} import *'.format(module, f.replace('.py', '')))
        return imports

    @staticmethod
    def check_and_add_init_py(path, skip_root=False):
        """
        Checks if __init__.py is in all subdirs under the given path

        :param path: root of the path where to begin
        :param skip_root: Whether to skip the root directory
        :return: list of paths for created __init__.py files
        """
        files = []

        for (dirpath, dirnames, filenames) in os.walk(path, followlinks=True):
            if skip_root and dirpath == path:
                continue

            # skip hidden directories and their subdirs
            dirs = [x for x in dirpath.replace(path, '').split(os.sep) if x.startswith('.')]
            if dirs:
                logger.debug("Skipping, since dirpath '%s' contains hidden dir: %s", dirpath, str(dirs))
                continue

            if '__init__.py' not in filenames:
                new_file = os.path.join(dirpath, '__init__.py')
                logger.debug("Creating __init__.py inside '%s'", dirpath)
                files.append(new_file)
                with open(new_file, 'w') as f:
                    f.write('# -*- coding: utf-8 -*-\n# File generated by Containers Testing Framework\n')
        return files

    def _combine_steps(self):
        """
        Generate steps.py inside the working_dir/steps/ which imports everything from

        :return:
        """
        steps_py_content = """# -*- coding: utf-8 -*-
# This file is automatically generated by Containers Testing Framework
# Any changes to this file will be discarded

from behave import *
""".splitlines()

        imports = self.get_import_statements(self._steps_dir)
        logger.debug("Using steps imports: %s", str(imports))
        steps_py_content.extend(imports)

        added_files = self.check_and_add_init_py(self._steps_dir)
        logger.debug("Created __init__.py files: %s", str(added_files))

        # create the steps.py
        with open(os.path.join(self._steps_dir, 'steps.py'), 'w') as f:
            logger.debug("Writing '%s'", os.path.join(self._steps_dir, 'steps.py'))
            f.write('\n'.join(steps_py_content) + '\n')


class BehaveRunner(object):
    """
    Class wrapping the process of running behave inside the working directory
    """

    def __init__(self, working_dir, cli_config):
        """
        Constructor

        :param working_dir: The BehaveWorkingDirectory instance
        :param cli_config: The CTFCliConf instance
        :return: None
        """
        self._working_dir_obj = working_dir
        self._cli_conf_obj = cli_config

    def run(self):
        """
        Run Behave and pass some runtime arguments
        :return:
        """
        command = [
            'behave',
            '-D DOCKERFILE={0}'.format(self._cli_conf_obj.get(CTFCliConfig.GLOBAL_SECTION_NAME,
                                                              CTFCliConfig.CONFIG_DOCKERFILE)),
            '-D IMAGE={0}'.format(self._cli_conf_obj.get(CTFCliConfig.GLOBAL_SECTION_NAME,
                                                         CTFCliConfig.CONFIG_IMAGE))
        ]

        logger.debug("Running behave: %s", str(command))

        return call(command, cwd=self._working_dir_obj.path())
