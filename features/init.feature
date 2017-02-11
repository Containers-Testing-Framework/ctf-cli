Feature: Initialize a new repo

  @xfail
  Scenario: Directory is not under git control
    Given a new working directory
    When I run "ctf init"
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

  Scenario: Tests dir already exists
    Given a new working directory
      And a directory named "tests"
    When I run "git init"
     And I run "ctf init"
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

  Scenario: Tests/features dir already exists
    Given a new working directory
      And a directory named "tests"
      And a directory named "tests/features"
    When I run "git init"
     And I run "ctf init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory tests already exists
        INFO:	Directory tests/features already exists
        INFO:	Creating tests/steps directory
        INFO:	Creating tests/steps/__init__.py file
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """

  Scenario: Tests/steps dir already exists
    Given a new working directory
      And a directory named "tests"
      And a directory named "tests/steps"
    When I run "git init"
     And I run "ctf init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory tests already exists
        INFO:	Creating tests/features directory
        INFO:	Directory tests/steps already exists
        INFO:	Creating tests/steps/__init__.py file
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """

  Scenario: Tests/steps/__init__.py already exists
    Given a new working directory
      And a directory named "tests"
      And a directory named "tests/steps"
      And an empty file named "tests/steps/__init__.py"
    When I run "git init"
     And I run "ctf init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory tests already exists
        INFO:	Creating tests/features directory
        INFO:	Directory tests/steps already exists
        INFO:	File tests/steps/__init__.py already exists
        INFO:	Creating tests/steps/steps.py file
        INFO:	Creating ctf.conf file
        """

  Scenario: Tests/steps/steps.py already exists
    Given a new working directory
      And a directory named "tests"
      And a directory named "tests/steps"
      And an empty file named "tests/steps/__init__.py"
      And an empty file named "tests/steps/steps.py"
    When I run "git init"
     And I run "ctf init"
    Then it should pass with:
        """
        INFO:	Initialize default directory structure
        INFO:	Directory tests already exists
        INFO:	Creating tests/features directory
        INFO:	Directory tests/steps already exists
        INFO:	File tests/steps/__init__.py already exists
        INFO:	File tests/steps/steps.py already exists
        INFO:	Creating ctf.conf file
        """

  Scenario: Tests config already exists
    Given a new working directory
      And an empty file named "ctf.conf"
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
        INFO:	File ctf.conf already exists
        """

  @xfail
  Scenario: ctf-cli is an alias
    Given a new working directory
    When I run "git init"
     And I run "ctf-cli init"
    Then it should pass with:
        """
        INFO: Initialize default directory structure
        INFO: Creating tests directory
        INFO: Creating tests/features directory
        INFO: Creating tests/steps directory
        INFO: Creating tests/steps/__init__.py file
        INFO: Creating tests/steps/steps.py file
        INFO: Creating ctf.conf file
        """
