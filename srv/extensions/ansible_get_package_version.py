#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

# -- config --
# description: A proof of concept that can trigger an ansible playbook called package_version.yml to get info about a specific package version
# param: package - The package to retrieve the information about
# http_method: post
# lock: False
# -- config --

from extension import CmdRun, Constants
from extension import ParamHandle as Param
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
print("{return} ansible_options={opt}".format(
  return=Constants.API_RETURN_STRING,
  opt=ansible_opts))
print(output)

exit(0)
