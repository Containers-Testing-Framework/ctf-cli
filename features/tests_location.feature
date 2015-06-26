Feature: Tests lookup

  Background:
    Given a new working directory
    When I successfully run "git init"
     And I successfully run "ctf-cli init"
     And I successfully run "ctf-cli remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf-cli remote add features https://github.com/Containers-Testing-Framework/common-features.git"

  Scenario: Default - run from 'tests' directory
    Given a directory named "tests"
     When I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        INFO:	Using project specific Features from 'tests/features'
        INFO:	Using project specific Steps from 'tests/steps'
        """

  Scenario: Run from 'test' directory
    When I rename the directory "tests" to "test"
     And I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        INFO:	Using project specific Features from 'test/features'
        INFO:	Using project specific Steps from 'test/steps'
        """

  @xfail
  # This might actually be broken
  Scenario: Run from execution directory
    When I move the directory "tests/features" to "."
     And I move the directory "tests/steps" to "."
     And I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        INFO:	Using project specific Features from 'features'
        INFO:	Using project specific Steps from 'steps'
        """