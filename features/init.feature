Feature: Initialize a new repo

  @xfail
  Scenario: Directory is not under git control
    Given a new working directory
    When I run "ctf-cli init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory is not under git control, running git init
        INFO:	Creating tests directory
        INFO:	Creating tests/features directory
        INFO:	Creating tests/steps directory
        INFO:	Creating tests/steps/__init__.py file
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """

  Scenario: Directory is under git control
    Given a new working directory
    When I run "git init"
     And I run "ctf-cli init"
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

  Scenario: Tests dir already exists
    Given a new working directory
      And a directory named "tests"
    When I run "git init"
     And I run "ctf-cli init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory tests already exists
        INFO:	Creating tests/features directory
        INFO:	Creating tests/steps directory
        INFO:	Creating tests/steps/__init__.py file
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """