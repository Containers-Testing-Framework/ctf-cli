# Containers Testing Framework CLI
Containers Testng Framework (CTF) is a simple wrapper around [Behave testing framework](http://pythonhosted.org/behave/). Behave is promissing approach for testing containers, since it enables one to focus on describing the behavior of the container from High Level and in simple English. For more information on how to use Behave and how to write tests using Behave, please reffer to the Behave project page.

CTF tries to reuse the remote execution of steps model from [UATFramework](https://github.com/aweiteka/UATFramework) so the tests can be executed locally or on remote machine or VM. The support is still in progress.

### The CTF provides:
- way for running tests on Dockerfiles and images
- way to run project-specific tests (Steps and Features)
- combination of multiple tests (Steps and Features) stored in remote repository
- ability to run remote tests on specific Dockerfile and/or image without having any project-specific tests suite

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

The best way to leverage the framework is to implement Features and Steps that are common for a set of containser as a remote tests and then just include it in the testing configuration of all containers.

### features/
Place any features and scenarios, specific for your particular container inside this directory. Your scenarios can use any of the steps implemented inside `tests/steps` directory or steps from any remote test you listed inside the `tests.conf` file. CTF CLI tool will combine all these steps together, so that Behave is able to find them when run.

### steps/
Place any steps that are specific for your features inside this directory. To make sure the steps can be executed on the remote machine or locally, always use `context.run()` for running any commands. In the background, the command will be run locally or on remote machine, based on the CLI configuration.

The CLI tool passes some runtime arguments to Behave, when executing it. The values are available through the context as `context.config.userdata` dictionary like object. To learn more about it, please read the [Behave documentation](http://pythonhosted.org/behave/new_and_noteworthy_v1.2.5.html#userdata).The following values are passed:

#### DOCKERFILE
This option contains the absolute path to Dockerfile wich should be tested. It is always set.

#### IMAGE
This option contains the name of the image to test. It is passed and set only if the name was passed to CLI tool using `-i` option.

### tests.conf
The `tests.conf` file contains configuration telling the CTF what extra remote tests (Steps and Features) to include when testing the container using Behave. It is a simple INI file. Each remote test needs to have its own section and inside the section specify `Steps` and `Features` options. These has to point to remote git repositories containing the appropriate Steps and Features. Example of tests.conf:

    [common-tests]
    Steps=https://github.com/Containers-Testing-Framework/common-steps.git
    Features=https://github.com/Containers-Testing-Framework/common-features.git

### environment.py
You can implement some of the methods that are typically used with Behave inside this file. It will be combined with the CTF common `environment.py` file. This integration may not be perfect yet, feel free to test and provide feedback.

## CLI tool
The key part of the framework is the CLI tool called `ctf-cli`. It gathers information, reads configurations, sets up the environment for Behave and runs it.

### Requirements
* git
* behave >= 1.2.5
* ansible

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
- Improve the handling of environment.py and provide some standard API, so the developer can add extra code to any standard method used in environment.py.
- Integrate the framework with some CI
- Add support for other ways of running command remotely besides ansible
- Add remote hosts provisioning, startng, stopping
 - support this for cloud, VMs, Vagrant boxes, etc.

## References
- [Behave](http://pythonhosted.org/behave/index.html)
- [UATFramework](https://github.com/aweiteka/UATFramework)
- [Behavior Driven Development](http://en.wikipedia.org/wiki/Behavior-driven_development)
