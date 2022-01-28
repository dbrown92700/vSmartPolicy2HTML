# SD-WAN vSmartPolicy2HTML [![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoSE/vSmartPolicy2HTML)

## Description

Simplifies viewing and navigating large vSmart CLI policies.

This python script will convert a vSmart CLI policy into an HTML page with hyperlinks to the different elements of the policy.

## Output Screenshot

![Screen Shot of Output](https://user-images.githubusercontent.com/46031546/151491354-90871e7e-5599-41ca-843b-9a1972744c6f.png)

## Instructions

Save vSmart policy as a .txt file.

NOTE: The script relies on space indents to correctly parse the configuration.  It expects that "policy" and "apply-policy" will have no spaces and each subsequent section or setting heirachy is indented by a single additional space.  This should be the standard CLI output.  Any issues with this indentation may cause the  parsing to fail.

NOTE: The script has not been tested against all potential policy elements.

NOTE: Do not include the full vSmart configuration.  This will parse only the policy.

Execute the script.  The name of the policy file can be passed as an option or the user will be prompted for the file name.  Examples:

> python3 policy2html.py

or

> ./policy2html.py sample-policy.txt
