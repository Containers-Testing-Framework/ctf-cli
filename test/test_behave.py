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
from .base_test import BaseTest
from ctf_cli.behave import BehaveWorkingDirectory


class TestBehaveWorkingDirectory(BaseTest):

    def test_get_import_statements(self):
        """
        Test that import statements are generated correctly
        :return:
        """
        dirs = [
            'myproj/common',
            'myproj/specific',
            'yourproj',
            'theirproj/common',
            'theirproj/common/steps',
            'theirproj/specific',
            'theirproj/.git',
            'theirproj/.git/dir',
        ]

        files = [
            'myproj/common/file1.py',
            'myproj/common/file2.py',
            'myproj/specific/your.py',
            'yourproj/step.py',
            'theirproj/common/file3.py',
            'theirproj/common/file4.py',
            'theirproj/common/steps/file5.py',
            'theirproj/common/steps/file6.py',
            'theirproj/common/steps/file7.py',
        ]

        expected_out = [
            'from myproj.common.file1 import *',
            'from myproj.common.file2 import *',
            'from myproj.specific.your import *',
            'from yourproj.step import *',
            'from theirproj.common.file3 import *',
            'from theirproj.common.file4 import *',
            'from theirproj.common.steps.file5 import *',
            'from theirproj.common.steps.file6 import *',
            'from theirproj.common.steps.file7 import *',
        ]

        # create dirs
        for d in dirs:
            os.makedirs(d)

        # create files
        for f in files:
            with open(f, 'w') as fw:
                fw.write(f)

        output = BehaveWorkingDirectory.get_import_statements(os.getcwd())
        assert len(set(expected_out).intersection(output)) == len(expected_out)

    def test_check_and_add_init_py(self):
        """
        Test that __init__.py is created in all directories in which it was missing
        :return:
        """
        dirs = [
            'myproj/common',
            'myproj/specific',
            'yourproj',
            'theirproj/common',
            'theirproj/common/steps',
            'theirproj/specific',
            'theirproj/.git',
            'theirproj/.git/dir',
        ]

        files = [
            # 'myproj/__init__.py'
            'myproj/common/__init__.py',
            # 'myproj/specific/__init__.py',
            'yourproj/__init__.py',
            'theirproj/__init__.py',
            # 'theirproj/common/__init__.py',
            'theirproj/common/steps/__init__.py',
            # 'theirproj/specific/__init__.py',
        ]

        f = [
            'myproj/__init__.py',
            'myproj/specific/__init__.py',
            'theirproj/common/__init__.py',
            'theirproj/specific/__init__.py',
        ]

        files_to_check = [os.path.join(self.WORKING_DIR, x) for x in f]

        # create dirs
        for d in dirs:
            os.makedirs(d)

        # create files
        for f in files:
            with open(f, 'w') as fw:
                fw.write(f)

        output = BehaveWorkingDirectory.check_and_add_init_py(os.getcwd())
        print(output)
        assert len(set(files_to_check).intersection(output)) == len(files_to_check)

        for f in files_to_check:
            assert os.path.exists(f)

    def test_find_tests_config_none(self):
        """
        Test that if no configuration file is present, None is returned
        :return:
        """
        assert BehaveWorkingDirectory.find_tests_config(self.WORKING_DIR) is None

    def test_find_tests_config_existing(self):
        """
        Test that configuration files are successfully found
        :return:
        """

        files = [
            'test.ini',
            'tests.ini',
            'test.conf',
            'tests.conf',
        ]

        for f in files:
            with open(f, 'w') as fw:
                fw.write('xyz')
            assert BehaveWorkingDirectory.find_tests_config(self.WORKING_DIR) == os.path.join(self.WORKING_DIR, f)
            os.remove(f)
            assert not os.path.exists(f)

    def test_find_tests_config_multiple(self):
        """
        Test that configuration files are found and that .ini has preference
        :return:
        """
        files = [
            'test.ini',
            'tests.conf',
        ]

        for f in files:
            with open(f, 'w') as fw:
                fw.write('xyz')

        assert BehaveWorkingDirectory.find_tests_config(self.WORKING_DIR) == os.path.join(self.WORKING_DIR, files[0])
