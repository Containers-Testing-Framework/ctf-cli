Feature: Run parameters

  Background:
    Given a new working directory
    When I successfully run "git init"
     And I successfully run "ctf init"
     And I successfully run "ctf remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf remote add features https://github.com/Containers-Testing-Framework/common-features.git"
     And I create a file named "tests/environment.py" with
     """
     from steps.common_steps.common_environment import docker_setup
     def before_all(context):
        docker_setup(context)
     """

  Scenario: Verbose
    When I successfully run "ctf -v run"
    Then the command output should contain:
        """
        INFO:	Running behave inside working directory 'behave -v
        """

  Scenario: Junit
    When I successfully run "ctf -v run -j junit_results_dir"
    Then the command output should contain:
        """
        INFO:	Running behave inside working directory 'behave -v --junit --junit-directory=junit_results_dir
        """
     And the directory "workdir/junit_results_dir" should exist

  Scenario: Behave data
    When I successfully run "ctf run --behave-data FOO=Bar"
    Then the command output should contain:
        """
        INFO:	Running behave inside working directory 'behave -D FOO=Bar
        """

  Scenario: Behave tags (no verbose)
    When I successfully run "ctf run --behave-tags tag1 --behave-tags ~tag2"
    Then the command output should contain:
        """
        INFO:	Running behave inside working directory 'behave -t tag1 -t ~tag2 --no-skipped -D
        """

  Scenario: Behave tags with verbose
    When I successfully run "ctf -v run --behave-tags tag1 --behave-tags ~tag2"
    Then the command output should contain:
        """
        INFO:	Running behave inside working directory 'behave -v -t tag1 -t ~tag2 -D
        """

  Scenario: Run with existing work directory
    Given a directory named "workdir"
     When I successfully run "ctf -v run"
     Then the command output should contain:
        """
        DEBUG:	Working directory '{__WORKDIR__}/workdir' exists. Removing it!
        DEBUG:	Creating working directory '/tmp/__WORKDIR__/workdir'.
        """
