#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi: set ft=python :
# Copyright 2016, Jonathan Kelley
#
# License: the mit license
#    Permission is hereby granted, free of charge, to any person obtaining a copy of
#    this software and associated documentation files (the "Software"), to deal in
#    the Software without restriction, including without limitation the rights to
#    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#    the Software, and to permit persons to whom the Software is furnished to do so,
#    subject to the above copyright notice and this permission notice shall being included
#    in all copies or substantial portions of the Software.

from extension import ParamHandle as Param
from extension import Script as script
import os

param = Param()  # <class> Parameter manipulation
parameters = param.list()  # <dict>   Input params list
parameters["EXTENSION_METADATA"] = {
    'entry': 'testentry.py', 'options': {'hello': 'world', 'test': {'k': 'v'}}}

print("The input params")
import json
print(json.dumps(parameters, indent=2))
print(json.dumps(dict(parameters['EXTENSION_METADATA']), indent=3))


def save_data():
    """
    Saves data about the script
    """
    save_list = {}
    for key in script_list:
        save_list[key] = {
            'trigger_settings': script_list[key].get_trigger_settings(),
            'enabled': script_list[key].is_enabled(),
            'next_run': script_list[key].get_next_run()
        }
    with open('data.json', 'w') as outfile:
        json.dump(save_list, outfile)


def load_data():
    with open('data.json') as data_file:
        data = json.load(data_file)
    return data

script_list = {}


def add_scripts(scriptsdir):
    print("Adding scripts from {scriptsdir}".format(scriptsdir=scriptsdir))
    for each_file in os.listdir(scriptsdir):
        file_name = os.path.splitext(os.path.basename(each_file))
        if file_name[1] == ".py" \
                and each_file != "__init__.py" \
                and each_file != "template.py":
            script_name = file_name[0]
            if script_name not in script_list.keys():
                script_list[script_name] = script(script_name)

    output, return_val = script_list[script_name].run()
    print("XXXXX")
    print(output)
    log_.warning('Run (' + script_name + '): ' +
                 str(return_val) + ' - ' + output)
    return json.dumps({'output': output, 'return': return_val})

print(add_scripts(os.path.dirname(os.path.realpath(__file__))))
