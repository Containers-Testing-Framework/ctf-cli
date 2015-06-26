Feature: Run parameters

  Background:
    Given a new working directory
    When I successfully run "git init"
     And I successfully run "ctf-cli init"
     And I successfully run "ctf-cli remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf-cli remote add features https://github.com/Containers-Testing-Framework/common-features.git"
     And I create a file named "tests/environment.py" with
     """
     from steps.common_steps.common_environment import docker_setup
     def before_all(context):
        docker_setup(context)
     """

  Scenario: Missing config
   Given I ensure that the file "~/ctf.conf" does not exist
     And I ensure that the file "~/.ctf/ctf.conf" does not exist
     And I ensure that the file "ctf.conf" does not exist
    When I run "ctf-cli -v run"
    Then it should fail with:
        """
        Didn't find any tests configuration file!
        """

  Scenario: Cli config in $HOME
   Given I ensure that the file "~/ctf.conf" does not exist
    When I move the file "ctf.conf" to "~"
     And I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        Using configuration from '{__HOME__}/ctf.conf'
        """

  Scenario: Cli config in $HOME/.ctf/
    Given a directory outside the workdir named "~/.ctf"
      And I ensure that the file "~/ctf.conf" does not exist
      And I ensure that the file "~/.ctf/ctf.conf" does not exist
    When I move the file "ctf.conf" to "~/.ctf/"
     And I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        Using configuration from '{__HOME__}/.ctf/ctf.conf'
        """