Feature: Smoke test

Scenario: Init, add remote, update and run
    Given a new working directory
    When I run "git init"
     And I run "ctf init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Creating tests directory
        INFO:	Creating tests/features directory
        INFO:	Creating tests/steps directory
        INFO:	Creating tests/steps/__init__.py file
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """
    When I run "ctf remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
    Then it should pass with:
        """
        Cloning into 'tests/steps/common_steps'...
        """
    When I run "ctf remote add features https://github.com/Containers-Testing-Framework/common-features.git"
    Then it should pass with:
        """
        Cloning into 'tests/features/common_features'...
        """
    When I run "ctf update"
    Then it should pass with:
        """
        Entering 'tests/features/common_features'
        Current branch master is up to date.
        Entering 'tests/steps/common_steps'
        Current branch master is up to date.
        INFO:	Updating remote test and features
        """
    When I create a file named "tests/environment.py" with
     """
     from steps.common_steps.common_environment import docker_setup
     def before_all(context):
        docker_setup(context)
     """
     And I successfully run "ctf run"
    Then the command output should contain:
        """
        INFO:	Running Containers Testing Framework cli
        INFO:	Using project specific Features from 'tests/features'
        INFO:	Using project specific Steps from 'tests/steps'
        """
