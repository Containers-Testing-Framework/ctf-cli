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
import tempfile


class BaseTest(object):
    """
    Base class for test. Will setup temporary environment in tmp for each test and destroy
    it aster test is finished.
    """
    WORKING_DIR = ''
    TESTS_DIR = os.path.join(os.getcwd(), 'test')

    def setup(self):
        """
        Setup the temporary environment and change the working directory to it.
        """
        self.WORKING_DIR = tempfile.mkdtemp(prefix="ctf-cli-test-")
        os.chdir(self.WORKING_DIR)

    def teardown(self):
        """
        Destroy the temporary environment.
        :return:
        """
        os.chdir(self.TESTS_DIR)
        shutil.rmtree(self.WORKING_DIR)