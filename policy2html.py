#!/usr/bin/env python3
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
__author__ = "David Brown <davibrow@cisco.com>"
__contributors__ = []
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import sys

action_sections = ['match', 'set', 'action', 'sequence', 'local-tloc-list']
policy_elements = {'sla-class': 'SC',
                   'data-policy': 'DP',
                   'data-prefix-list': 'DPL',
                   'prefix-list': 'PL',
                   'tloc-list': 'TL',
                   'app-list': 'AL',
                   'color-list': 'CL',
                   'site-list': 'SL',
                   'control-policy': 'CP',
                   'app-route-policy': 'ARP',
                   'cflowd-template': 'CT',
                   'vpn-list': 'VL'}


def policy_to_html(input_file):

    # Read the config into a list

    file = open(input_file)
    config = file.readlines()
    file.close()

    #
    # Pass 1: Parse the file for all section elements and put them in a list
    #

    elements = {}

    for lineNum, line in enumerate(config):
        if line == 'apply-policy\n':
            config[lineNum] = '<a id="apply-policy"><b>apply-policy</b></a>\n'
            break
        if not ('!' in line):   # Skip lines with !

            # calculate the indent on this line vs. the next line
            leader = line.count(' ') - line.lstrip(' ').count(' ')
            nextline = config[lineNum + 1]
            leader_next = nextline.count(' ') - nextline.lstrip(' ').count(' ')

            # Track if we're parsing the lists section of the config
            if leader == 1:
                if line == ' lists\n':
                    lists_section = True
                else:
                    lists_section = False

            if leader_next > leader:  # This is a section line
                if ' ' in line.lstrip(' '):  # This has a name
                    line_split = line.lstrip(' ').rstrip('\n').split()
                    if (line_split[0] in action_sections) or ((not lists_section) and (line_split[0] == 'vpn-list')):
                        pass
                    else:
                        if not line_split[0] in elements:
                            elements[line_split[0]] = []
                        elements[line_split[0]].append(line_split[1])
                        config[lineNum] = leader * ' ' + \
                                          f'{line_split[0]} <a id="{policy_elements[line_split[0]]}:{line_split[1]}">' \
                                          f'<b>{line_split[1]}'\
                                          + '</b></a>'

    #
    # Pass 2: Parse the file and link all references to the elements in the list
    #

    apply_section = False
    for lineNum, line in enumerate(config):

        if '!' in line:
            continue

        if 'apply-policy' in line:
            apply_section = True

        leader = line.count(' ') - line.lstrip(' ').count(' ')
        if leader == 1:
            if line == ' lists\n':
                lists_section = True
            else:
                lists_section = False

        nextline = config[lineNum + 1]
        leader_next = nextline.count(' ') - nextline.lstrip(' ').count(' ')
        line_split = line.lstrip(' ').rstrip('\n').split()
        if (not (leader_next > leader))\
                or apply_section\
                or ((not lists_section) and (line_split[0] == 'vpn-list')):  # This is a config element
            for index, keyword in enumerate(line_split):
                for element_type, instances in elements.items():
                    if keyword in instances:
                        if element_type in line_split[index - 1]:
                            line_split[index] = f'<a href="#{policy_elements[element_type]}:{keyword}">{keyword}'\
                                               + '</a>'
                            break
            config[lineNum] = leader * ' ' + ' '.join(line_split)

    #
    # Create html file of the policy
    #

    outfile = open(f'{input_file.rstrip(".txt")}.html', 'w')
    outfile.write('<html><body>\n<h1>Policy Elements</h1>\n')
    outfile.write('<h2>Apply Policy Section</h2><a href="#apply-policy">apply-policy</a><br>')

    # Create table of contents for policy elements
    for element_type, instances in elements.items():
        outfile.write(f'<h2>{element_type}'+'</h2>\n')
        for line in instances:
            outfile.write(f'<a href="#{policy_elements[element_type]}:{line}">{line}</a><br>\n')

    # Write the policy
    outfile.write('<h1>Policy</h1>\n')
    for index, line in enumerate(config):
        leader = line.count(' ') - line.lstrip(' ').count(' ')
        line = leader * '&nbsp;' * 3 + line.lstrip(' ')
        outfile.write(f'{index}:{line}'+'<br>\n')
    outfile.write('</html></body>')
    outfile.close()

    return elements


if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input('Name of policy file: ')

    output = policy_to_html(filename)
