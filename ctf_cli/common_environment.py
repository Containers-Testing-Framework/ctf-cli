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
# GNU General Public License for more d`etails.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

sample_ctl_ctf_config = """
[ctf]
#Verbose=yes
#CLIConfPath=/etc/ctf.conf
#TestsConfigPath=/etc/ctf-tests.conf
#Dockerfile=/home/user/my_cool_project/Dockerfile
#Image=centos:centos7
ExecType=ansible

[ansible]
Host=192.168.1.1
Method=local
User=root
"""

common_steps_py_content = """# -*- coding: utf-8 -*-
from common_steps.common_connection_steps import *
from common_steps.common_docker_steps import *
"""
