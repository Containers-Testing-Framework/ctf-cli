# -*- coding: utf-8 -*-
#
# Simple DNS Proxy for simulating DNS issues
# Copyright (C) 2014-2015  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:

import os
import six
from six.moves.configparser import ConfigParser

from ctf_cli.logger import logger


class CTFCliConfig(object):
    """
    Configuration parser for CTF CLI
    """

    GLOBAL_SECTION_NAME = 'ctf_cli'
    CONFIG_VERBOSE = 'Verbose'
    CONFIG_CLI_CONFIG_PATH = 'CLIConfigPath'
    CONFIG_TESTS_CONFIG_PATH = 'TestsConfigPath'
    CONFIG_DOCKERFILE = 'Dockerfile'
    CONFIG_IMAGE = 'Image'

    def __init__(self, cli_conf):
        self._config = ConfigParser()
        self._add_commandline_arguments(cli_conf)



        config_abs_path = os.path.abspath(cli_conf.cli_config_path)

        try:
            self._config.read(config_abs_path)[0]
        except IndexError:
            logger.debug("Configuration file '%s' could not be read... "
                         "Using ONLY default settings", config_abs_path)
        else:
            logger.debug("Using configuration from '%s'", config_abs_path)

    def _add_commandline_arguments(self, cli_conf):
        """
        Construct a dict from CLI arguments and add it to Config

        :param cli_conf: ArgumentParser object initialized by CLI args
        :return: None
        """
        cli_settings = {self.GLOBAL_SECTION_NAME: {
            self.CONFIG_VERBOSE: 'yes' if cli_conf.verbose else 'no',
            self.CONFIG_CLI_CONFIG_PATH: os.path.abspath(cli_conf.cli_config_path),
            self.CONFIG_TESTS_CONFIG_PATH: os.path.abspath(
                cli_conf.tests_config_path)if cli_conf.tests_config_path else None,
            self.CONFIG_DOCKERFILE: os.path.abspath(
                cli_conf.dockerfile) if cli_conf.dockerfile else None,
            self.CONFIG_IMAGE: cli_conf.image
        }}

        self.config_parser_read_dict(self._config, cli_settings)

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

    @staticmethod
    def config_parser_read_dict(config_parser_obj, dictionary):
        """
        Read dictionary into the ConfigParser. Existing values in ConfigParser
        object are not overwritten. (note: read_dict() is not available in Python 2.7)

        :param config_parser_obj: existing ConfigParser object
        :param dictionary: dictionary to read the config from {<section>: {<option>: <value>, ...}}
        :return: None
        """
        # go through all sections
        for section, conf in six.iteritems(dictionary):
            if config_parser_obj.has_section(section) is False:
                config_parser_obj.add_section(section)

            # go through all key: value in the section
            for option, value in six.iteritems(conf):
                if config_parser_obj.has_option(section, option) is False:
                    config_parser_obj.set(section, option, value)