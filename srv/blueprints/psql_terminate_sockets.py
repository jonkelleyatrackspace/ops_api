#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: Will terminate sockets to a user or a database.
# param: user - If supplied, will terminate all connections to this user.
# param: database -  If supplied, will terminate all connections to this database.
# param: application -  If supplied, will terminate all connections to this appliccation.
# param: pid -  If supplied, will terminate all connections to this pid.
# param: client_address -  If supplied, will terminate all connections to this IP.
# http_method: post
# lock: False
# tags: Postgres, Psql
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

param = "database"
database = Param()
database.value = params[param]
database.name = param
database.max_length = Constants.POSTGRES_NAMEDATA_LEN
database.sanitizier = "sql"
database.set_value_if_defined()
sanitized_arguement[param] = database.get()

param = "application"
application = Param()
application.value = params[param]
application.name = param
application.max_length = Constants.POSTGRES_NAMEDATA_LEN
application.sanitizier = "sql"
application.set_value_if_defined()
sanitized_arguement[param] = application.get()

param = "user"
user = Param()
user.value = params[param]
user.name = param
user.max_length = Constants.POSTGRES_NAMEDATA_LEN
user.sanitizier = "sql"
user.set_value_if_defined()
sanitized_arguement[param] = user.get()

param = "pid"
pid = Param()
pid.value = params[param]
pid.name = param
pid.max_length = Constants.POSTGRES_NAMEDATA_LEN
pid.sanitizier = "sql"
pid.set_value_if_defined()
sanitized_arguement[param] = pid.get()

param = "client_address"
clientaddr = Param()
clientaddr.value = params[param]
clientaddr.name = param
clientaddr.max_length = Constants.POSTGRES_NAMEDATA_LEN
clientaddr.sanitizier = "sql"
clientaddr.set_value_if_defined(True)
sanitized_arguement[param] = clientaddr.get()

if sanitized_arguement['database']:
    arg_identifier = "datname"
    arg_key = database.value
elif sanitized_arguement['application']:
    arg_identifier = "application_name"
    arg_key = application.value
elif sanitized_arguement['user']:
    arg_identifier = "usename"
    arg_key = user.value
elif sanitized_arguement['pid']:
    arg_identifier = "procpid"
    arg_key = pid.value
elif sanitized_arguement['client_address']:
    arg_identifier = "client_addr"
    arg_key = clientaddr.value
else:
    toolkit.print_stderr(
        "Must provide at least 1 parameter to kill connections by.")
    exit(1)


# ******************
# *  SQL SENTENCE  *
# ******************
clean_sql = ("SELECT row_to_json(t)  FROM ("
             "    SELECT pg_terminate_backend(pid)"
             "     FROM pg_stat_activity"
             "       WHERE {identifier} = '{key}'"
             ") as t; ;"
             ).format(identifier=real_escape_string.sql(arg_identifier), key=real_escape_string.sql(arg_key))
toolkit.fail_beyond_maxlength(maxlength=1000, string=clean_sql)
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

# Process result
for line in output.split(linesep):
    if line == "ROLLBACK":
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if "psql:/tmp/" in line and " ERROR:  " in line:
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL:  " in line and "terminating connection due" in line:
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if "connection unexpectedly" in line or "terminated abnormally" in line:
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if "connection to server" in line and "lost" in line:
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
    print("return_value execution_status=ok")
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_2:
        error_hint.append('SQL_ERROR')
    if error_scenario_3:
        error_hint.append('CLIENT_SOCKET_WAS_TERMINATED')
    if error_scenario_4:
        error_hint.append('FATAL_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("return_value execution_status=rollback")
    print("return_value error_reason_indicator={error}".format(
        error=error_hint))

toolkit.exit(exitcode)
