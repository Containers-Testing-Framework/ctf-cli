# -*- coding -*-
import os.path
from steps.__setup import TOP, HERE
from subprocess import check_call


def after_all(context):
    check_call('coverage combine', cwd=TOP, shell=True)
    repo = os.path.normpath('%s/../..' % HERE)
    check_call('mv .coverage %s' % repo, cwd=TOP, shell=True)
