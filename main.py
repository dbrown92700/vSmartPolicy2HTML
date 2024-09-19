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

from flask import Flask, request, render_template, redirect, flash
from markupsafe import Markup


upload_folder = '/tmp'
allowed_extensions = {'txt'}

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOAD_FOLDER'] = upload_folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


action_sections = ['match', 'set', 'action', 'sequence', 'local-tloc-list', 'customized-ipv4-record-fields']
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
                   'vpn-list': 'VL',
                   'community-list': 'CmL',
                   'vpn-membership': 'VPN'
                   }


def policy_to_html(config):

    #
    # Pass 1: Parse the file for all section elements and put them in a list
    #

    elements = {}
    lists_section = False

    for lineNum, line in enumerate(config):
        if lineNum == len(config)-1:
            break
        if '!' in line:
            continue
        if 'apply-policy' in line:
            config[lineNum] = '<a id="apply-policy"><b>apply-policy</b></a>\n'
            break

        # calculate the indent on this line vs. the next line
        leader = line.count(' ') - line.lstrip(' ').count(' ')
        nextline = config[lineNum + 1]
        leader_next = nextline.count(' ') - nextline.lstrip(' ').count(' ')

        # Track if we're parsing the lists section of the config
        if leader == 1:
            if ' lists' in line:
                lists_section = True
            else:
                lists_section = False

        if leader_next > leader:  # This is a section line
            if ' ' in line.lstrip(' '):  # This has a name
                line_split = line.lstrip(' ').rstrip('\n').split()
                if (line_split[0] in action_sections) or ((not lists_section) and (line_split[0] == 'vpn-list')):
                    pass
                else:
                    print(line_split)
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
        if lineNum == len(config)-1:
            break
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

    outfile = '<html><body>\n<h1>Policy Elements</h1>\n'
    outfile += '<h2>Apply Policy Section</h2><a href="#apply-policy">apply-policy</a><br>' \

    # Create table of contents for policy elements
    for element_type, instances in elements.items():
        outfile += f'<h2>{element_type}'+'</h2>\n'
        for line in instances:
            outfile += f'<a href="#{policy_elements[element_type]}:{line}">{line}</a><br>\n'

    # Write the policy
    outfile += '<h1>Policy</h1>\n'
    for index, line in enumerate(config):
        leader = line.count(' ') - line.lstrip(' ').count(' ')
        line = leader * '&nbsp;' * 3 + line.lstrip(' ')
        outfile += f'{index}:{line}'+'<br>\n'
    outfile += '</html></body>'

    return outfile


@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and not allowed_file(file.filename):
            flash('File must have a .txt extension')
            return redirect(request.url)
        else:
            file_text = file.read()
            config = file_text.decode('utf-8').split('\n')
            converted_config = policy_to_html(config)
            return Markup(converted_config)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
