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
import logging
from ctf_cli import settings


class LoggerHelper(object):
    """
    Helper class for setting up a logger
    """

    @staticmethod
    def get_basic_logger(logger_name, level=logging.DEBUG):
        """
        Sets-up a basic logger without any handler

        :param logger_name: Logger name
        :param level: severity level
        :return: created logger
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        return logger

    @staticmethod
    def add_stream_handler(logger, formatter=None, level=None):
        """
        Adds console handler with given severity.

        :param logger: logger object to add the handler to
        :param level: severity level
        :return: None
        """
        console_handler = logging.StreamHandler()
        if level:
            console_handler.setLevel(level)
        if formatter:
            console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    @staticmethod
    def add_file_handler(logger, path, formatter=None, level=None):
        """
        Adds FileHandler to a given logger

        :param logger: Logger object to which the file handler will be added
        :param path: Path to file where the debug log will be written
        :return: None
        """
        file_handler = logging.FileHandler(path, 'w')
        if level:
            file_handler.setLevel(level)
        if formatter:
            file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    @staticmethod
    def add_debug_log_file(path=''):
        """
        Add the application wide debug log file
        :return:
        """
        debug_log_file = os.path.join(path, settings.DEBUG_LOG_FILE_NAME)
        try:
            LoggerHelper.add_file_handler(logger,
                                          debug_log_file,
                                          logging.Formatter("%(asctime)s %(levelname)s\t%(filename)s"
                                                            ":%(lineno)s %(funcName)s: %(message)s"),
                                          logging.DEBUG)
        except (IOError, OSError):
            logger.warning("Can not create debug log '%s'", debug_log_file)


#  the main Containers Testing Framework CLI logger
logger = LoggerHelper.get_basic_logger('ctf-cli')
