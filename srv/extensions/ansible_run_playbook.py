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
# param: playbook - The path to the playbook you wish to run with ansible
# param: ask_valt_pass - When true, ask for vault password
# param: check - When true, don't make any changes
# param: diff - When true, when changing (small) files and templates, show the  differences in those files
# param: extra_vars - set additional variables as key=value or YAML/JSON
# param: flush_cache - when true, clear fact cache
# param: force_handlers - run handlers even if a task fails
# param: forks - specify number of parallel processes to use
# param: help - When true, shows ansible help message
# param: inventory_file - specify inventory host path default=/etc/ansible/hosts
# param: limit - limit query to specific set of subset hosts
# param: list_tasks - when true, just list all tasks that would be executed
# param: list_tags - When true, list all available tags
# param: list_hosts - When true, outputs a list of matching hosts; does not execute
# param: new_vault_password - New vault password file for rekey
# param: output - output file name for encrypt or decrypt; use '—' for stdout
# param: skip_tags - Only run plays and tasks whose tags do not match these
# param: vault_password_file - Vault password file
# param: verbose - When true, verbose mode, when any other value set ——vvvv (debug)
# param: version -  When true, show program's version number and exit
# param: ask_pass -  When true, ask for connection password
# param: private_key -  Use this file to authenticate the connection
# param: user -  Connect as this user (default=None)
# param: conection -  Connection type to use (default=smart)
# param: timeout -  Override the connection timeout in seconds (default=15)
# param: sudo -  Run operations with sudo (nopasswd) (deprecated, use become)
# param: sudo_user -  Desired sudo user (default=root) (deprecated, use become)
# param: su  -  Run operations with su as this user (default=root)
# param: become -  When true, run operations with become
# param: become_method -  Privilege escalation method to use (default=sudo)
# param: become_user -  When true, run operations with become (does not imply password prompt)
# param: ask_sudo_pass -  When true, ask for sudo password (deprecated, use become)
# param: ask_su_pass -  When true, ask for su password (deprecated, use become)
# param: ask_become_pass -  When true, ask for privilege escalation password
# http_method: post
# lock: False
# -- config --

from os import linesep
from extension import Sanitize, CmdRun
from extension import ToolKit, Constants
from extension import ParamHandle as Param


# Spawn Instances
p = Param()                       # <class> Parameter manipulation
real_escape_string = Sanitize()   # <class> Escape Routines
toolkit = ToolKit()               # <class> Misc. functions
params = p.list()                 # <dict>   Input params list
run = CmdRun()                    # <class> Runs the query


# ************************************
# *  DEFINE PARAMETERS AND VALIDATE  *
# ************************************
sanitized_arguement = {} # The actual API params we pass to psql

param = "playbook"
playbook = Param()
playbook.value = params[param]
playbook.name = param
playbook.max_length = Constants.LINUX_MAX_FILE_PATH_LENGTH
playbook.require = True
sanitized_arguement[param] = playbook.get()

param = "ask_valt_pass"
ask_valt_pass = Param()
ask_valt_pass.value = params[param]
ask_valt_pass.name = param
ask_valt_pass.max_length = 6
ask_valt_pass.set_value_if_defined("--ask_valt_pass",custom_else_value="")
sanitized_arguement[param] = ask_valt_pass.get()

param = "check"
check = Param()
check.value = params[param]
check.name = param
check.max_length = 6
ask_valt_pass.set_value_if_defined("--check",custom_else_value="")
sanitized_arguement[param] = check.get()

param = "diff"
diff = Param()
diff.value = params[param]
diff.name = param
diff.max_length = 6
ask_valt_pass.set_value_if_defined("--diff",custom_else_value="")
sanitized_arguement[param] = diff.get()

param = "diff"
diff = Param()
diff.value = params[param]
diff.name = param
diff.max_length = 6
ask_valt_pass.set_value_if_defined("--diff",custom_else_value="")
sanitized_arguement[param] = diff.get()

param = "extra_vars"
extra_vars = Param()
extra_vars.value = params[param]
extra_vars.name = param
extra_vars.max_length = 6
ask_valt_pass.set_value_if_defined("--extra_vars",custom_else_value="")
sanitized_arguement[param] = extra_vars.get()

param = "flush_cache"
flush_cache = Param()
flush_cache.value = params[param]
flush_cache.name = param
flush_cache.max_length = 6
ask_valt_pass.set_value_if_defined("--flush_cache",custom_else_value="")
sanitized_arguement[param] = flush_cache.get()

param = "force_handlers"
value_when_true = " --force_handlers {z} ".format(z=params[param])
value_when_false = ""
force_handlers = Param()
force_handlers.value = params[param]
force_handlers.name = param
force_handlers.max_length = Constants.POSTGRES_NAMEDATA_LEN
force_handlers.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = force_handlers.get()

param = "forks"
value_when_true = " --forks {z} ".format(z=params[param])
value_when_false = ""
forks = Param()
forks.value = params[param]
forks.name = param
forks.max_length = Constants.POSTGRES_NAMEDATA_LEN
forks.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = forks.get()

param = "help"
helpflg = Param()
helpflg.value = params[param]
helpflg.name = param
helpflg.max_length = 6
ask_valt_pass.set_value_if_defined("--help",custom_else_value="")
sanitized_arguement[param] = helpflg.get()

param = "inventory_file"
value_when_true = " --inventory_file {z} ".format(z=params[param])
value_when_false = ""
inventory_file = Param()
inventory_file.value = params[param]
inventory_file.name = param
inventory_file.max_length = Constants.POSTGRES_NAMEDATA_LEN
inventory_file.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = inventory_file.get()

param = "limit"
value_when_true = ' --limit \"{z}\" '.format(z=params[param])
value_when_false = ""
limit = Param()
limit.value = params[param]
limit.name = param
limit.max_length = Constants.POSTGRES_NAMEDATA_LEN
limit.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = limit.get()

param = "list_tasks"
list_tasks = Param()
list_tasks.value = params[param]
list_tasks.name = param
list_tasks.max_length = 6
ask_valt_pass.set_value_if_defined("--list_tasks",custom_else_value="")
sanitized_arguement[param] = list_tasks.get()

param = "list_tags"
list_tags = Param()
list_tags.value = params[param]
list_tags.name = param
list_tags.max_length = 6
ask_valt_pass.set_value_if_defined("--list_tags",custom_else_value="")
sanitized_arguement[param] = list_tags.get()

param = "help"
list_hosts = Param()
list_hosts.value = params[param]
list_hosts.name = param
list_hosts.max_length = 6
ask_valt_pass.set_value_if_defined("--list_hosts",custom_else_value="")
sanitized_arguement[param] = list_hosts.get()

param = "new_vault_password"
value_when_true = " --new_vault_password {z} ".format(z=params[param])
value_when_false = ""
new_vault_password = Param()
new_vault_password.value = params[param]
new_vault_password.name = param
new_vault_password.max_length = Constants.POSTGRES_NAMEDATA_LEN
new_vault_password.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = new_vault_password.get()

param = "output"
value_when_true = " --output {z} ".format(z=params[param])
value_when_false = ""
output = Param()
output.value = params[param]
output.name = param
output.max_length = Constants.POSTGRES_NAMEDATA_LEN
output.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = output.get()

param = "skip_tags"
value_when_true = " --skip_tags {z} ".format(z=params[param])
value_when_false = ""
skip_tags = Param()
skip_tags.value = params[param]
skip_tags.name = param
skip_tags.max_length = Constants.POSTGRES_NAMEDATA_LEN
skip_tags.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = skip_tags.get()

param = "vault_password_file"
value_when_true = " --vault_password_file {z} ".format(z=params[param])
value_when_false = ""
vault_password_file = Param()
vault_password_file.value = params[param]
vault_password_file.name = param
vault_password_file.max_length = Constants.POSTGRES_NAMEDATA_LEN
vault_password_file.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = vault_password_file.get()

param = "verbose"
verbose = Param()
verbose.value = params[param]
verbose.name = param
verbose.max_length = 6
ask_valt_pass.convert_to_bool(
  custom_whentrue_value=" -v ",
  custom_whenfalse_value="",
  custom_badinput_value=" -vvvv "
  )
sanitized_arguement[param] = verbose.get()

param = "version"
version = Param()
version.value = params[param]
version.name = param
version.max_length = 6
version.set_value_if_defined("--version",custom_else_value="")
sanitized_arguement[param] = version.get()

param = "ask_pass"
ask_pass = Param()
ask_pass.value = params[param]
ask_pass.name = param
ask_pass.max_length = 6
ask_pass.set_value_if_defined("--ask_pass",custom_else_value="")
sanitized_arguement[param] = ask_pass.get()

param = "private_key"
value_when_true = " --private_key {z} ".format(z=params[param])
value_when_false = ""
private_key = Param()
private_key.value = params[param]
private_key.name = param
private_key.max_length = Constants.POSTGRES_NAMEDATA_LEN
private_key.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = private_key.get()

param = "user"
value_when_true = " --connection {z} ".format(z=params[param])
value_when_false = ""
user = Param()
user.value = params[param]
user.name = param
user.max_length = Constants.POSTGRES_NAMEDATA_LEN
user.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = user.get()

param = "user"
value_when_true = " --user {z} ".format(z=params[param])
value_when_false = ""
connection = Param()
connection.value = params[param]
connection.name = param
connection.max_length = Constants.POSTGRES_NAMEDATA_LEN
connection.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = connection.get()

param = "timeout"
value_when_true = " --timeout {z} ".format(z=params[param])
value_when_false = ""
timeout = Param()
timeout.value = params[param]
timeout.name = param
timeout.max_length = Constants.POSTGRES_NAMEDATA_LEN
timeout.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = timeout.get()

param = "sudo"
value_when_true = " --sudo {z} ".format(z=params[param])
value_when_false = ""
sudo = Param()
sudo.value = params[param]
sudo.name = param
sudo.max_length = Constants.POSTGRES_NAMEDATA_LEN
sudo.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = sudo.get()

param = "sudo_user"
value_when_true = " --sudo_user {z} ".format(z=params[param])
value_when_false = ""
sudo_user = Param()
sudo_user.value = params[param]
sudo_user.name = param
sudo_user.max_length = Constants.POSTGRES_NAMEDATA_LEN
sudo_user.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = sudo_user.get()

param = "su"
value_when_true = " --su {z} ".format(z=params[param])
value_when_false = ""
su = Param()
su.value = params[param]
su.name = param
su.max_length = Constants.POSTGRES_NAMEDATA_LEN
su.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = su.get()

param = "ask_pass"
ask_pass = Param()
ask_pass.value = params[param]
ask_pass.name = param
ask_pass.max_length = 6
ask_pass.set_value_if_defined("--ask_pass",custom_else_value="")
sanitized_arguement[param] = ask_pass.get()

param = "become"
become = Param()
become.value = params[param]
become.name = param
become.max_length = 6
become.set_value_if_defined("--become",custom_else_value="")
sanitized_arguement[param] = become.get()

param = "become"
become = Param()
become.value = params[param]
become.name = param
become.max_length = 6
become.set_value_if_defined("--become",custom_else_value="")
sanitized_arguement[param] = become.get()

param = "become_method"
value_when_true = " --become_method {z} ".format(z=params[param])
value_when_false = ""
become_method = Param()
become_method.value = params[param]
become_method.name = param
become_method.max_length = Constants.POSTGRES_NAMEDATA_LEN
become_method.set_value_if_defined(value_when_true, value_when_false)
sanitized_arguement[param] = become_method.get()

param = "ask_sudo_pass"
ask_sudo_pass = Param()
ask_sudo_pass.value = params[param]
ask_sudo_pass.name = param
ask_sudo_pass.max_length = 6
ask_valt_pass.set_value_if_defined("--ask_sudo_pass",custom_else_value="")
sanitized_arguement[param] = ask_sudo_pass.get()

param = "ask_su_pass"
ask_su_pass = Param()
ask_su_pass.value = params[param]
ask_su_pass.name = param
ask_su_pass.max_length = 6
ask_su_pass.set_value_if_defined("--ask_su_pass",custom_else_value="")
sanitized_arguement[param] = ask_su_pass.get()

param = "ask_become_pass"
ask_become_pass = Param()
ask_become_pass.value = params[param]
ask_become_pass.name = param
ask_become_pass.max_length = 6
ask_become_pass.set_value_if_defined("--ask_become_pass",custom_else_value="")
sanitized_arguement[param] = ask_become_pass.get()


# ****************************
# *  DEFINE ANSIBLE OPTIONS  *
# ****************************
# This will set or override the options inputted by the API user.
# Special (non arguements) include:
#  - ansible_opts['playbook'] which is the path to the playbook file

sanitized_arguement['--limit'] = '\"vagrant\"'
sanitized_arguement['--inventory-file'] = '/opt/playbooks/ansible-hosts'
sanitized_arguement['--user'] = 'vagrant'


# *****************
# *  RUN ANSIBLE  *
# *****************
output = run.ansible(sanitized_arguement)


# *************
# *  RESULTS  *
# *************
print(output)
print("return_value ansible_options={opt}".format(opt=ansible_opts))
exit(0)
