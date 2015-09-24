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

import sys
import os

from ctf_cli.arguments_parser import ArgumentsParser
from ctf_cli.application import Application
from ctf_cli.logger import logger, LoggerHelper, logging
from ctf_cli.exceptions import CTFCliError


class CliRunner(object):
    """
    Entry point class for command line
    """

    @staticmethod
    def run():
        try:
            # add application-wide debug log
            LoggerHelper.add_debug_log_file(os.getcwd())
            args = ArgumentsParser(sys.argv[1:])
            if args.verbose is True:
                LoggerHelper.add_stream_handler(logger,
                                                logging.Formatter('%(levelname)s:\t%(message)s'),
                                                logging.DEBUG)
            else:
                LoggerHelper.add_stream_handler(logger,
                                                logging.Formatter('%(levelname)s:\t%(message)s'),
                                                logging.INFO)

            app = Application(args)
            if 'init' in args.cli_action:
                app.init()
            if 'run' in args.cli_action:
                app.run()
            if 'update' in args.cli_action:
                app.update()
            if 'remote' in args.cli_action:
                if 'add' in args.remote_action:
                    app.add_remote()
                if 'remove' in args.remote_action:
                    app.remove_remote()
                if 'list' in args.remote_action:
                    app.list_remotes()

        except KeyboardInterrupt:
            logger.info('Interrupted by user')
        except CTFCliError as e:
            logger.error('%s', str(e))
            sys.exit(1)
        else:
            sys.exit(0)
        finally:
            logger.debug('Exiting...')


def run():
    CliRunner.run()
