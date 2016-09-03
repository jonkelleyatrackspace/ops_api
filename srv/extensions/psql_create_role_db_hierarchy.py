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
# description: Creates a specified database with specified role and super-role, as well as a specified super_svc and _svc account pair. Uses PostgreSQL+Database+References+and+Standards.
# param: application - The name of your application. It will be application_role and accounts will be named after it.
# param: super_svc_login - If the super svc has login permission
# param: super_maxsock - Super svc maximum sockets
# param: super_password - Super svc password
# param: svc_login - If the svc account has login permission
# param: svc_maxsock - Svc account maximum sockets
# param: svc_password - Svc account password
# http_method: post
# lock: False
# tags: Postgres, CREATEAPPTIER, Psql
# -- config --

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

param = "application"
application = Param()
application.value = params[param]
application.name = param
application.max_length = Constants.POSTGRES_NAMEDATA_LEN
application.require = True
application.sanitizier = "sql"
sanitized_arguement[param] = application.get()

param = "super_password"
super_password = Param()
super_password.value = params[param]
super_password.name = param
super_password.max_length = Constants.POSTGRES_NAMEDATA_LEN
super_password.require = True
super_password.sanitizier = "sql"
sanitized_arguement[param] = super_password.get()


param = "svc_password"
svc_password = Param()
svc_password.value = params[param]
svc_password.name = param
svc_password.max_length = Constants.POSTGRES_NAMEDATA_LEN
svc_password.require = True
svc_password.sanitizier = "sql"
sanitized_arguement[param] = svc_password.get()

param = "super_svc_login"
super_svc_login = Param()
super_svc_login.value = params[param]
super_svc_login.name = param
super_svc_login.max_length = Constants.POSTGRES_NAMEDATA_LEN
super_svc_login.sanitizier = "sql"
sanitized_arguement[param] = super_svc_login.get()

param = "super_svc_login"
sql_when_true = " LOGIN ".format(verb=param.upper())
sql_when_false = " NOLOGIN ".format(verb=param.upper())
super_svc_login = Param()
super_svc_login.value = params[param]
super_svc_login.name = param
super_svc_login.max_length = Constants.POSTGRES_NAMEDATA_LEN
super_svc_login.sanitizier = "sql"
super_svc_login.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = super_svc_login.get()

param = "super_maxsock"
val_when_nil = " 3 "
val_when_not = " {x} ".format(x=params[param])
super_maxsock = Param()
super_maxsock.value = params[param]
super_maxsock.name = param
super_maxsock.max_length = Constants.POSTGRES_NAMEDATA_LEN
super_maxsock.sanitizier = "sql"
super_maxsock.set_value_if_undefined(
    custom_if_value=val_when_nil, custom_else_value=val_when_not)
sanitized_arguement[param] = super_maxsock.get()

param = "svc_login"
sql_when_true = " LOGIN ".format(verb=param.upper())
sql_when_false = " NOLOGIN ".format(verb=param.upper())
svc_login = Param()
svc_login.value = params[param]
svc_login.name = param
svc_login.max_length = Constants.POSTGRES_NAMEDATA_LEN
svc_login.sanitizier = "sql"
svc_login.convert_to_bool(sql_when_true, sql_when_false, sql_when_false)
sanitized_arguement[param] = svc_login.get()

param = "svc_maxsock"
val_when_nil = " 2 "
val_when_not = " {x} ".format(x=params[param])
svc_maxsock = Param()
svc_maxsock.value = params[param]
svc_maxsock.name = param
svc_maxsock.max_length = Constants.POSTGRES_NAMEDATA_LEN
svc_maxsock.sanitizier = "sql"
svc_maxsock.set_value_if_undefined(
    custom_if_value=val_when_nil, custom_else_value=val_when_not)
sanitized_arguement[param] = svc_maxsock.get()


# ******************
# *  SQL SENTENCE  *
# ******************
clean_sql = (
    "\echo on\n"
    "BEGIN;\n"
    "/* Make super role  */\n"
    "CREATE  ROLE  {myapplication}_super_role  NOLOGIN;\n"
    "COMMIT;\n"
    "\n"
    "/* Make database (owned by) super role  */\n"
    "CREATE  DATABASE  {myapplication}  OWNER  {myapplication}_super_role;\n"
    "\n"
    "BEGIN;\n"
    "/* Make SUPER service account  */\n"
    "CREATE  ROLE  {myapplication}_super_svc \n"
    "  {super_login} INHERIT CONNECTION LIMIT{super_maxsock}  PASSWORD  '{super_password}'\n"
    "    IN ROLE  {myapplication}_super_role;\n"
    "\n"
    "/*  Make ROLE for application  */\n"
    "CREATE ROLE  {myapplication}_role  NOLOGIN;\n"
    "\n"
    "/* Make ROLE for application service account */\n"
    "CREATE  ROLE  {myapplication}_svc \n"
    "  {svc_login} INHERIT CONNECTION LIMIT {svc_maxsock}  PASSWORD  '{svc_password}'\n"
    "    IN ROLE  {myapplication}_role;\n"
    "COMMIT;\n"
).format(
    myapplication=sanitized_arguement['application'],
    super_password=sanitized_arguement['super_password'],
    super_login=sanitized_arguement['super_svc_login'],
    super_maxsock=sanitized_arguement['super_maxsock'],
    svc_login=sanitized_arguement['svc_login'],
    svc_maxsock=sanitized_arguement['svc_maxsock'],
    svc_password=sanitized_arguement['svc_password']
)
toolkit.fail_beyond_maxlength(maxlength=1500, string=clean_sql)
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
    if ("ERROR:" in line) and (" database " in line) and ("already exists" in line):
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if (line == "ROLLBACK") or ("transaction is aborted, commands ignored" in line):
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if ("psql:/tmp/" in line) and (" ERROR:  " in line):
        toolkit.print_stderr(line)
        error_scenario_4 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL: " in line:
        toolkit.print_stderr(line)
        error_scenario_5 = True
        exitcode = 1  # Parse Errors should flag an API error code.

# Report Output
if exitcode == 0:
    # We good
    print("return_value execution_status=ok")
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('ROLE_ALREADY_EXIST')
    if error_scenario_2:
        error_hint.append('DATABASE_ALREADY_EXIST')
    if error_scenario_3:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_4:
        error_hint.append('SQL_ERROR')
    if error_scenario_5:
        error_hint.append('FATAL_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("return_value execution_status=rollback")
    print("return_value error_reason_indicator={error}".format(
        error=error_hint))

toolkit.exit(exitcode)