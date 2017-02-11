Feature: Remote functions

  Background:
    Given a new working directory
    When I successfully run "git init"
     And I successfully run "ctf init"

  Scenario: Remote add steps
    When I successfully run "ctf remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
    Then the directory "tests/steps/common_steps" exists

  Scenario: Remote add features
    When I successfully run "ctf remote add features https://github.com/Containers-Testing-Framework/common-features.git"
    Then the directory "tests/features/common_features" exists

  Scenario: List remotes
    When I successfully run "ctf remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf remote add features https://github.com/Containers-Testing-Framework/common-features.git"
    When I run "ctf remote list"
    Then it should pass with:
        """
        https://github.com/Containers-Testing-Framework/common-features.git
        https://github.com/Containers-Testing-Framework/common-steps.git
        """

  Scenario: Remove remote
    When I successfully run "ctf remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf remote add features https://github.com/Containers-Testing-Framework/common-features.git"
     And I successfully run "ctf remote remove tests/features/common_features"
    When I run "ctf remote list"
    Then it should pass with:
        """
        https://github.com/Containers-Testing-Framework/common-steps.git
        """
     And the directory "tests/features/common_features" should not exist
