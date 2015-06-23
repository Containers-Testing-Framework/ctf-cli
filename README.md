# Containers Testing Framework CLI

[![Circle CI](https://circleci.com/gh/Containers-Testing-Framework/ctf-cli.svg?style=svg)](https://circleci.com/gh/Containers-Testing-Framework/ctf-cli)[![Code Health](https://landscape.io/github/Containers-Testing-Framework/ctf-cli/master/landscape.svg?style=flat)](https://landscape.io/github/Containers-Testing-Framework/ctf-cli/master)[![Coverage Status](https://coveralls.io/repos/vrutkovs/ctf-cli/badge.svg?branch=ci)](https://coveralls.io/r/vrutkovs/ctf-cli?branch=ci)

[![Join the chat at https://gitter.im/Containers-Testing-Framework/ctf-cli](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Containers-Testing-Framework/ctf-cli?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Containers Testing Framework (CTF) is a simple wrapper around [Behave testing framework](http://pythonhosted.org/behave/). Behave is a promising approach for testing containers, since it enables one to focus on describing the behavior of the container from a High Level and in simple English. For more information on how to use Behave and how to write tests using Behave, please refer to the Behave project page.

CTF tries to re-use the remote execution of steps model from [UATFramework](https://github.com/aweiteka/UATFramework) so the tests can be executed locally or on a remote machine or VM. The support is still in progress.

### CTF provides:
- a way of running tests on Dockerfiles and images
- a way to run project-specific tests (Steps and Features)
- a combination of multiple tests (Steps and Features) stored in remote repository
- the ability to run remote tests on specific Dockerfiles and/or images without having any project-specific tests suite

## How to use the framework for your containers?

If you want to implement project-specific tests, you should create the following directory structure inside your project directory `my_project_dir`:

    my_project_dir/
      tests/
        features/
          my_cool.feature
          my_other_cool.feature
        steps/
          my_cool_steps.py
          my_other_cool_steps.py
        environment.py
        tests.conf

The best way to leverage the framework is to implement Features and Steps that are common for a set of containers as a remote test and then include it in the testing configuration of all containers.

### features/
Place any features and scenarios, specific for your particular container inside this directory. Your scenarios can use any of the steps implemented inside `tests/steps` directory or steps from any remote test you listed inside the `tests.conf` file. CTF CLI tool will combine all these steps together, so that Behave is able to find them when run.

### steps/
Place any steps that are specific for your features inside this directory. To make sure the steps can be executed on the remote machine or locally, always use `context.run()` for running any commands. In the background, the command will be run locally or on remote machine, based on the CLI configuration.

The CLI tool passes some runtime arguments to Behave, when executing it. The values are available through the context as `context.config.userdata` dictionary like object. To learn more about it, please read the [Behave documentation](http://pythonhosted.org/behave/new_and_noteworthy_v1.2.5.html#userdata). The following values are passed:

#### DOCKERFILE
This option contains the absolute path to the Dockerfile wich should be tested. It is always set.

#### IMAGE
This option contains the name of the image to test. It is passed and set only if the name was passed to CLI tool using `-i` option.

### tests.conf
The `tests.conf` file contains configuration telling the CTF what extra remote tests (Steps and Features) to include when testing the container using Behave. It is a simple INI file. Each remote test needs to have its own section and inside the section specify `Steps` and `Features` options. These has to point to remote git repositories containing the appropriate Steps and Features. Example of tests.conf:

    [common-tests]
    Steps=https://github.com/Containers-Testing-Framework/common-steps.git
    Features=https://github.com/Containers-Testing-Framework/common-features.git

#### This method is not recommended and will soon be deprecated - git submodules way would be preferred


### environment.py
You can implement any of the methods that are typically used with Behave inside this file. They will be combined with the CTF common `environment.py` file. And your methods will be invoked before the CTF hooks.

## Getting Started

### Requirements
* git
* behave >= 1.2.5
* ansible

### Installation

1. Clone repositories
```
git clone https://github.com/Containers-Testing-Framework/ctf-cli.git
```
1. Optional: clone an example repository
```
git clone https://github.com/Containers-Testing-Framework/example-project-postgresql.git
```
1. Change to ctf-cli directory
```
cd ctf-cli
```
1. Install python dependencies
```
[sudo] pip install -r requirements.txt
```
1. Copy sample configuration files and edit as necessary
```
cp ctf.conf.sample ctf.conf
cp tests.conf.sample tests.conf
```
1. Change to project directory and get common features
```
cd example-project-postgresql
../ctf-cli/ctf-cli.py remote add features https://github.com/Containers-Testing-Framework/common-features.git
```
1. Run tests
```
../ctf-cli/ctf-cli.py run
```

## CLI tool
The key part of the framework is the CLI tool called `ctf-cli`. It gathers information, reads configurations, sets up the environment for Behave and runs it. Currently `ctf-cli` tool supports only ansible for running commands on some host. To run your tests make sure you included configuration for ansible in the `ctf-cli` configuration.


### Configuration file
You can pass the path to the configuration file on the command line using the `-c` or `--cli-config` option. If not provided the tool tries to find the configuration in this order of preference:

1. `ctf.conf` in the current directory
2. `ctf.conf` in the user home directory `~/ctf.conf`
3. `ctf.conf` in the `ctf` direcotory inside user home directory `~/ctf/ctf.conf`
4. `ctf.conf` in the system configuration directory `/etc/ctf.conf`

The configuration must include configuration for ansible. The setup on the host you want to use needs to be done manually before running the `ctf-cli` (e.g. setting up ssh keys, etc.) An example of the configuration for ansible inside the `ctf.conf` can look like this:

    [ansible]
    Host=127.0.0.1
    User=root
    Method=ssh

### Usage
The `ctf-cli` should be executed inside the directory of the project, containing the Dockerfile. There are couple of options one can pass to the CLI tool:

- `-h`, `--help` - Prints the help message and exit
- `-v`, `--verbose` - Makes the output (much) more verbose (recommended)
- `-c CLI_CONFIG_PATH`, `--cli-config CLI_CONFIG_PATH` - Path to CLI configuration file (default: '/etc/ctf-cli.conf')
- `-t TESTS_CONFIG_PATH`, `--tests-config TESTS_CONFIG_PATH` - Path to tests configuration file. By default it will be searched for in tests/ dir
- `-f DOCKERFILE`, `--dockerfile DOCKERFILE` - Path to Dockerfile to use. If not passed, will be searched for in the current directory
- `-i IMAGE`, `--image IMAGE` - Image to use for testing. If not passed, the image will be built from the Dockerfile

### How it works?
When `ctf-cli` is executed in `my_proj_dir` project directory the following happens:

1. CLI tool configuration is read.
2. The directory is searched for the `tests/` directory.
3. The `tests/` directory is searched for `tests.conf` configuration.
4. A working directory `my_proj_dir-behave-working-dir` is created inside current directory.
5. `features` and `steps` directories are created inside the working directory.
6. Project specific features are copied into the `features/my_proj_dir_features` inside working directory.
7. Project specific steps are copied into the `steps/my_proj_dir_steps` inside working directory.
8. If environment.py is present in `tests/`, then it is copied into the working directory as `my_proj_dir_environment.py`.
9. If `tests.conf` contained some remote test, their Features and Steps are cloned into the working directory similarly as done for local files in (6.) and (7.).
10. Makes sure all subdirectories inside `steps/` in working directory contain `__init__.py`.
11. Create `steps.py` inside `steps/` in working directory, which imports everything from all steps files.
12. Create `environment.py` in working directory, which contains CTF common methods and includes the project specific environment.py file if present.
13. Run Behave inside the working directory with all the necessary runtime arguments

## Ideas for further development
- The steps done by CLI tool can be separated (prepare working dir, update working dir, run tests). This would allow one to do the partial workflow if needed.
- Using specific commit for remote tests. This prevents surprises when someone breaks tests shared across multiple containers.
- Testing containers combinations. Idea is to tag the containers by some roles (e.g. @webserver, @database, ...) and then access these containers just based on the tags in the steps. This way any webserver could be tested with any database, and so on.
- Integrate the framework with some CI
- Add support for other ways of running command remotely besides ansible
- Add remote hosts provisioning, startng, stopping
 - support this for cloud, VMs, Vagrant boxes, etc.

## Decisions made
- we will go with submodules instead of tests.conf
- it is not acceptable to expect users to directly call git - needed functionality has to be wrapped by CTF
- remote features/steps should be added into tests/remote/... to prevent conflicts with project-specific features/steps
- we will need export and import commands to export and import current project tests setup for sharing between projects
- we can not expect that the project is using git (maybe create git repo if not using git only in the tests/ dir?)
- tests.conf will be deprecated as it is used ATM
- the "generated" environment.py should be kept clean and all containers specific code should be moved elsewhere. 

## References
- [Behave](http://pythonhosted.org/behave/index.html)
- [UATFramework](https://github.com/aweiteka/UATFramework)
- [Behavior Driven Development](http://en.wikipedia.org/wiki/Behavior-driven_development)
