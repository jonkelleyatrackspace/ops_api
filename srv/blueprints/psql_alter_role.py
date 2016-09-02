#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: Perform ALTER on a ROLE
# param: role - Your ROLE name
# param: createrole - If bool set, Toggle CEATEROLE else NOCREATEROLE
# param: createuser - If bool set, Toggle CREATEUSER else NOCREATEUSER
# param: createdb - If bool set, Toggle CREATEDB else NOCREATEDB
# param: inherit - If bool set, Toggle INHERIT else NOINHERIT
# param: login - If bool set, Toggle LOGIN else NOLOGIN
# param: connection_limit - Maximum connections default is 10. Max is 25.
# param: connection_limit_bust - Raise to max_val(150)
# param: rolename - Which role (only one currently) to add to
# param: groupname -  Which group (only one currently) to add to
# http_method: post
# lock: False
# tags: Postgres, ALTERROLE, Psql
# -- jojo --

from os import linesep
from blueprint import Sanitize, CmdRun
from blueprint import ToolKit, Constants
from blueprint import ParamHandle as Param

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
role.sanitizier = "sql"
role.require = True
sanitized_arguement[param] = role.get()

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
connection_limit_bust.set_value_if_defined(True)  # Set to True is defined for bool comparisons
sanitized_arguement[param] = connection_limit_bust.get()

# Handling connection limit parsing requires advanced work
#  While imposing limits and limit busting...
phelper = Param()  # Using the parameter instance tools for validation.
if phelper.is_nil(sanitized_arguement['connection_limit']):
    # If no input, we plan on just setting 10 sockets.
    connection_limit = 10
elif sanitized_arguement['connection_limit_bust']:
    # Limit busting has been toggled
    if int(sanitized_arguement['connection_limit']) > Constants.POSTGRES_MAXIMUM_CONNECTION_LIMIT:
        # If the proposed limit is not beyond the POSTGRES_MAXIMUM_CONNECTION_LIMIT, stop
        # We expect a smaller value.
        msg = "value <{max}".format(
            max=Constants.POSTGRES_MAXIMUM_CONNECTION_LIMIT)
        phelper.raise_error(
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
        phelper.raise_error(
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
clean_sql = ("BEGIN; ALTER ROLE {rolname} WITH {connection_limit}{createuser}"
             "{createrole}{createdb}{inherit}{login}"
             " {inrole}{ingroup}; END;"
             ).format(
    rolname=sanitized_arguement['role'],
    createuser=sanitized_arguement['createuser'],
    createrole=sanitized_arguement['createrole'],
    createdb=sanitized_arguement['createdb'],
    inherit=sanitized_arguement['inherit'],
    login=sanitized_arguement['login'],
    connection_limit=real_escape_string.sql(arg_connlimit),
    inrole=sanitized_arguement['rolename'],
    ingroup=sanitized_arguement['groupname'],
)
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

for line in output.split(linesep):
    if line == "ROLLBACK":
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if "psql:/tmp/" in line and " ERROR:  " in line:
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if ("ERROR:" in line) and (" role " in line) and ("does not exist" in line):
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL: " in line:
        toolkit.print_stderr(line)
        error_scenario_4 = True
        exitcode = 1  # Parse Errors should flag an API error code.

# Report Output
if exitcode == 0:
    # We good
    print("jojo_return_value execution_status=ok")
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_2:
        error_hint.append('SQL_ERROR')
    if error_scenario_3:
        error_hint.append('ROLE_DOES_NOT_EXIST')
    if error_scenario_4:
        error_hint.append('FATAL_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    if error_scenario_3:
        error_hint.append('ROLE_DOES_NOT_EXIST')
    print("jojo_return_value execution_status=rollback")
    print("jojo_return_value error_reason_indicator={error}".format(
        error=error_hint))

toolkit.exit(exitcode)
