#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: A proof of concept that can trigger an ansible playbook called package_version.yml to get info about a specific package version
# param: package - The package to retrieve the information about
# http_method: post
# lock: False
# -- jojo --

from blueprint import CmdRun, Constants
from blueprint import ParamHandle as Param
from json import dumps as decode

# Spawn Instances
parameter2 = Param()    # <class> Parame ter manipulation
run = CmdRun()          # <class> Runs the query
params = parameter2.list()  # <dict>  A dict of params


# ************************************
# *  DEFINE PARAMETERS AND VALIDATE  *
# ************************************
arguement = {} # The actual API params we pass to psql

param = "package"
package = Param()
package.value = params[param]
package.name = param
package.require = True
package.max_length = Constants.LINUX_MAX_FILE_NAME_LENGTH
arguement[param] = {'package': package.get()}


# ****************************
# *  DEFINE ANSIBLE OPTIONS  *
# ****************************
# This will be used to define the argv keyvalue pairs passed to ansible.
# Special (non arguements) include:
#  - ansible_opts['playbook'] which is the path to the playbook file
#  - ansible_opts['append_args'] which value should include any appendable arg like -vvvv
ansible_opts = {}

ansible_opts['playbook'] = '/opt/playbooks/ansible-playbooks/package_version.yml'
ansible_opts['append_args'] = '-v'
ansible_opts['--limit'] = '\"vagrant\"'
ansible_opts['--inventory-file'] = '/opt/playbooks/ansible-hosts'
ansible_opts['--user'] = 'vagrant'
ansible_opts['--extra-vars'] = decode(arguement['package'])


# *****************
# *  RUN ANSIBLE  *
# *****************
output = run.ansible(ansible_opts)


# *************
# *  RESULTS  *
# *************
print("jojo_return_value ansible_options={opt}".format(opt=ansible_opts))
print(output)
exit(0)
