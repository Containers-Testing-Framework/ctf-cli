# Some useful functions for your environment.py
from types import ModuleType
import tempfile
import shutil
import ansible.runner
import logging
import re
import os
import glob
import stat
import inspect
import copy


def _invoke_other_environment_hooks(*args):
    # we need a copy of current frame becase it will change
    frame_globals = copy.copy(inspect.currentframe().f_globals)
    # get which function invoked us
    current_function = inspect.stack()[1][3]
    # iterate for all modules wich ends with _environemnt
    # and execute current method from them
    for g in frame_globals:
        if isinstance(frame_globals[g], ModuleType):
            if frame_globals[g].__name__.endswith("_environment"):
                for func_name, func in inspect.getmembers(frame_globals[g], inspect.isfunction):
                    if func_name == current_function:
                        func(*args)


def before_all(context):
    _invoke_other_environment_hooks(context)
    try:
        ansible_cfg = context.config.userdata['ANSIBLE']
        inventory = ansible.inventory.Inventory(ansible_cfg)
    except KeyError:
        raise Exception("-D ANSIBLE missing")
    remote_dir = '/tmp/'

    def open_file(path):
        context.temp_dir = tempfile.mkdtemp()
        ret = ansible.runner.Runner(
            module_name='fetch',
            inventory=inventory,
            module_args='src={0} dest={1}'.format(
                path, context.temp_dir)).run()
        for _, value in ret['contacted'].iteritems():
            try:
                ret_file = open(value['dest'])
                return ret_file
            except KeyError:
                print("ansible output: {0}".format(ret))
                raise Exception(value['msg'])
    context.open_file = open_file

    def run(command):
        if '{{' in command:
            command = command.replace("{{", "{{ '{{").replace("}}", "}}' }}")
        logging.info("Running '%s'", command)
        context.result = ansible.runner.Runner(
            module_name="shell",
            inventory=inventory,
            module_args="{0} chdir={1}".format(command, remote_dir)
        ).run()
        # dark means not responding
        if context.result['dark']:
            print(context.result)
        if not context.result['contacted']:
            print("no contacted hosts")
        for host, values in context.result['contacted'].iteritems():
            logging.info("On {0} returned {1}".format(host, values['rc']))

            if 'cmd' in values:
                logging.info("cmd: {0}".format(values['cmd']))
            if 'stderr' in values:
                logging.info('stderr:%s', values['stderr'])

            result = ''
            if 'msg' in values:
                logging.info('msg:%s', values['msg'])
                result = values['msg']
            if 'stdout' in values:
                logging.info('stdout:%s', values['stdout'])
                result = values['stdout']

            if values['rc'] != 0:
                assert False
            return result
    context.run = run

    def copy_dockerfile():

        try:
            # copy dockerfile
            dockerfile = context.config.userdata['DOCKERFILE']
            dockerfile_dir = os.path.dirname(dockerfile)
            # create remote directory
            ansible.runner.Runner(
                module_name='file',
                inventory=inventory,
                module_args='dest={0} state=directory'.format(remote_dir)
                ).run()
            # copy dockerfile
            ansible.runner.Runner(
                module_name='copy',
                inventory=inventory,
                module_args='src={0} dest={1}'.format(dockerfile, remote_dir)
                ).run()
            # copy files from dockerfile
            f_in = open(dockerfile)
            for path in re.findall('(?:ADD|COPY) ([^ ]+) ', f_in.read()):
                for glob_path in glob.glob(os.path.join(dockerfile_dir, path)):
                    # TODO Is there a nicer way to keep permissions?
                    ansible.runner.Runner(
                        module_name='copy',
                        inventory=inventory,
                        module_args='src={0} dest={1} directory_mode mode={2}'.format(
                            glob_path, remote_dir,
                            oct(stat.S_IMODE(os.stat(glob_path).st_mode)))
                    ).run()
        except Exception as e:
            logging.warning("copy_dockerfile:%s", e)

    copy_dockerfile()

    # build image if not exist
    try:
        context.image = context.config.userdata['IMAGE']
        run('docker pull {0}'.format(context.image))
    except AssertionError:
        pass
    except KeyError:
        context.image = 'ctf'
        try:
            run('docker build -t {0} .'.format(context.image))
        except AssertionError:
            pass

    cid_file_name = re.sub(r'\W+', '', context.image)
    context.cid_file = "/tmp/%s.cid" % cid_file_name


def after_scenario(context, scenario):
    _invoke_other_environment_hooks(context, scenario)
    try:
        if context.config.userdata['KEEP_CONTAINER_AFTER_TEST']:
            return
    except KeyError as e:
        pass

    try:
        cid = context.run('cat %s' % context.cid_file)
    except AssertionError as e:
        logging.info("after_scenario: %s", str(e))
        return
    if cid:
        context.run("docker logs %s" % cid)
        try:
            context.run("docker stop %s" % cid)
            context.run("docker kill %s" % cid)
            context.run("docker rm -v %s" % cid)
        except AssertionError:
            pass
        if hasattr(context, 'cid'):
            del context.cid
        context.run('rm {0}'.format(context.cid_file))


def after_all(context):
    _invoke_other_environment_hooks(context)
    if hasattr(context, 'temp_dir'):
        shutil.rmtree(context.temp_dir)  # FIXME catch exception
