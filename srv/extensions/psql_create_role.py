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
# description: Create a new ROLE in Postgres.
# param: role - Your ROLE name
# param: password - Role PASSWORD
# param: createrole - If bool set, Toggle CEATEROLE else NOCREATEROLE
# param: createuser - If bool set, Toggle CREATEUSER else NOCREATEUSER
# param: createdb - If bool set, Toggle CREATEDB else NOCREATEDB
# param: inherit - If bool set, Toggle INHERIT else NOINHERIT
# param: login - If bool set, Toggle LOGIN else NOLOGIN
# param: connection_limit - Maximum connections default is 10. Max is 25.
# param: connection_limit_bust - Raise to max_val(150)
# param: encrypted - If bool set, Toggle UNENCRYPTED else ENCRYPTED
# param: rolename - Which role (only one currently) to add to
# param: groupname -  Which group (only one currently) to add to
# http_method: post
# lock: False
# tags: Postgres, CREATEROLE, Psql
# -- end config --

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

param = "role"
role = Param()
role.value = params[param]
role.name = param
role.max_length = Constants.POSTGRES_NAMEDATA_LEN
role.require = True
role.sanitizier = "sql"
sanitized_arguement[param] = role.get()

param = "password"
password = Param()
password.value = params[param]
password.name = param
password.max_length = Constants.POSTGRES_NAMEDATA_LEN
password.require = True
password.sanitizier = "sql"
sanitized_arguement[param] = password.get()

param = "createrole"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " NO{verb} ".format(verb=param.upper())
createrole = Param()
createrole.value = params[param]
createrole.name = param
createrole.max_length = Constants.POSTGRES_NAMEDATA_LEN
createrole.sanitizier = "sql"
createrole.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = createrole.get()

param = "createuser"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " NO{verb} ".format(verb=param.upper())
createuser = Param()
createuser.value = params[param]
createuser.name = param
createuser.max_length = Constants.POSTGRES_NAMEDATA_LEN
createuser.sanitizier = "sql"
createuser.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = createuser.get()

param = "createdb"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " NO{verb} ".format(verb=param.upper())
createdb = Param()
createdb.value = params[param]
createdb.name = param
createdb.max_length = Constants.POSTGRES_NAMEDATA_LEN
createdb.sanitizier = "sql"
createdb.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = createdb.get()

param = "inherit"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " NO{verb} ".format(verb=param.upper())
inherit = Param()
inherit.value = params[param]
inherit.name = param
inherit.max_length = Constants.POSTGRES_NAMEDATA_LEN
inherit.sanitizier = "sql"
inherit.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = inherit.get()

param = "login"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " NO{verb} ".format(verb=param.upper())
login = Param()
login.value = params[param]
login.name = param
login.max_length = Constants.POSTGRES_NAMEDATA_LEN
login.sanitizier = "sql"
login.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = login.get()

param = "encrypted"
sql_when_true = " {verb} ".format(verb=param.upper())
sql_when_false = " UN{verb} ".format(verb=param.upper())
encrypted = Param()
encrypted.value = params[param]
encrypted.name = param
encrypted.max_length = Constants.POSTGRES_NAMEDATA_LEN
encrypted.sanitizier = "sql"
encrypted.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = encrypted.get()

param = "rolename"
sql_when_true = " IN ROLE {rolename} ".format(rolename=params[param])
sql_when_false = ""
rolename = Param()
rolename.value = params[param]
rolename.name = param
rolename.max_length = Constants.POSTGRES_NAMEDATA_LEN
rolename.sanitizier = "sql"
rolename.set_value_if_defined(sql_when_true, sql_when_false)
sanitized_arguement[param] = rolename.get()

param = "groupname"
sql_when_true = " IN GROUP {groupname} ".format(groupname=params[param])
sql_when_false = ""
groupname = Param()
groupname.value = params[param]
groupname.name = param
groupname.max_length = Constants.POSTGRES_NAMEDATA_LEN
groupname.sanitizier = "sql"
groupname.set_value_if_defined(sql_when_true, sql_when_false)
sanitized_arguement[param] = groupname.get()

param = "connection_limit"
connection_limit = Param()
connection_limit.value = params[param]
connection_limit.name = param
connection_limit.max_length = 3
connection_limit.sanitizier = "sql"
sanitized_arguement[param] = connection_limit.get()

param = "connection_limit_bust"
connection_limit_bust = Param()
connection_limit_bust.value = params[param]
connection_limit_bust.name = param
connection_limit_bust.sanitizier = "sql"
# Set to True is defined for bool comparisons
connection_limit_bust.set_value_if_defined(True)
sanitized_arguement[param] = connection_limit_bust.get()

# Handling connection limit parsing requires advanced work
#  While imposing limits and limit busting...
thisparam = Param()  # Using the parameter instance tools for validation.
if thisparam.is_nil(sanitized_arguement['connection_limit']):
    # If no input, we plan on just setting 10 sockets.
    connection_limit = 10
elif sanitized_arguement['connection_limit_bust']:
    # Limit busting has been toggled
    if int(sanitized_arguement['connection_limit']) > Constants.POSTGRES_MAXIMUM_CONNECTION_LIMIT:
        # If the proposed limit is not beyond the POSTGRES_MAXIMUM_CONNECTION_LIMIT, stop
        # We expect a smaller value.
        msg = "value <{max}".format(
            max=Constants.POSTGRES_MAXIMUM_CONNECTION_LIMIT)
        thisparam.raise_error(
            keyname='connection_limit',
            value=sanitized_arguement['connection_limit'],
            expected_msg=msg
        )
    # Set the busted limit
    connection_limit = sanitized_arguement['connection_limit']
else:
    # User-submitted connection limit (no limit busting)
    if int(sanitized_arguement['connection_limit']) > Constants.POSTGRES_CONNECTION_LIMIT:
        # If the proposed limit is beyond the POSTGRES_CONNECTION_LIMIT, stop
        # We expect a smaller value.
        msg = "value <{max}".format(max=Constants.POSTGRES_CONNECTION_LIMIT)
        thisparam.raise_error(
            keyname='connection_limit',
            value=sanitized_arguement['connection_limit'],
            expected_msg=msg
        )
    # Set the requested limit
    connection_limit = sanitized_arguement['connection_limit']
arg_connlimit = " CONNECTION LIMIT {max} ".format(max=connection_limit)


# ******************
# *  SQL SENTENCE  *
# ******************
clean_sql = ("BEGIN; CREATE ROLE {username} WITH {connection_limit}{createuser}"
             "{createrole}{createdb}{inherit}{login}{encrypted} PASSWORD '{password}'"
             " {inrole}{ingroup}; END;"
             ).format(
    username=real_escape_string.sql(sanitized_arguement['role']),
    password=real_escape_string.sql(sanitized_arguement['password']),
    createuser=real_escape_string.sql(sanitized_arguement['createuser']),
    createrole=real_escape_string.sql(sanitized_arguement['createrole']),
    createdb=real_escape_string.sql(sanitized_arguement['createdb']),
    inherit=real_escape_string.sql(sanitized_arguement['inherit']),
    login=real_escape_string.sql(sanitized_arguement['login']),
    connection_limit=real_escape_string.sql(arg_connlimit),
    encrypted=real_escape_string.sql(sanitized_arguement['encrypted']),
    inrole=real_escape_string.sql(sanitized_arguement['rolename']),
    ingroup=real_escape_string.sql(sanitized_arguement['groupname']),
)
# Fail if SQL overruns 2000 bytes
toolkit.fail_beyond_maxlength(maxlength=2000, string=clean_sql)
sql_code = toolkit.write_temp(clean_sql)


# ****************
# *  SQL RUNNER  *
# ****************
output = run.sql(sql_code)


# **********************
# *  OUTPUT PROCESSOR  *
# **********************
print(output)
exitcode = 0
error_scenario_1 = False
error_scenario_2 = False
error_scenario_3 = False
error_scenario_4 = False
error_scenario_5 = False

# Parse Output
for line in output.split(linesep):
    if ("ERROR:" in line) and (" role " in line) and ("already exists" in line):
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if (line == "ROLLBACK") or ("transaction is aborted, commands ignored" in line):
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if ("psql:/tmp/" in line) and (" ERROR:  " in line):
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL: " in line:
        toolkit.print_stderr(line)
        error_scenario_4 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if "syntax error" in line and "ERROR" in line:
        toolkit.print_stderr(line)
        error_scenario_5 = True
        exitcode = 1  # Parse Errors should flag an API error code.

# Report Output
if exitcode == 0:
    # We good
    print("{status}=ok".format(status=Constants.API_SUMMARY_STRING))
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('ROLE_ALREADY_EXIST')
    if error_scenario_2:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_3:
        error_hint.append('SQL_ERROR')
    if error_scenario_4:
        error_hint.append('FATAL_ERROR')
    if error_scenario_5:
        error_hint.append('SYNTAX_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("{status}=rollback".format(status=Constants.API_SUMMARY_STRING))
    print("{errors}={reasons}".format(reasons=error_hint,
        errors=Constants.API_ERROR_STRING))

toolkit.exit(exitcode)