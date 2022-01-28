# vSmartPolicy2HTML

## Description

Simplifies viewing and navigating large vSmart policies.

This python script will convert a vSmart CLI policy into an HTML page with hyperlinks to the different elements of the policy.

## Instructions

Save vSmart policy as a .txt file.

NOTE: The script relies on space indents to correctly parse the configuration.  It expects that "policy" and "apply-policy" will have no spaces and each subsequent section or setting heirachy is indented by a single additional space.  This should be the standard CLI output.  Any issues with this indentation may cause the  parsing to fail.

Execute the script.  The name of the policy file can be passed as an option or the user will be prompted for the file name.  Examples:

> python3 policy2html.py

or

> ./policy2html.py sample-policy.txt
