Feature: Run parameters

Scenario: Verbose
    Given a new working directory
    When I successfully run "git init"
     And I successfully run "ctf-cli init"
     And I successfully run "ctf-cli remote add steps https://github.com/Containers-Testing-Framework/common-steps.git"
     And I successfully run "ctf-cli remote add features https://github.com/Containers-Testing-Framework/common-features.git"
     And I successfully run "ctf-cli -v run"
    Then the command output should contain:
        """
        Using defaults:
        logging_format %(levelname)s:%(name)s:%(message)s
        """