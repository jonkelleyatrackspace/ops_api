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
# description: Create a new DATABASE in Postgres.
# param: database - Your ROLE name
# http_method: post
# lock: False
# tags: Postgres, CREATEROLE, Psql
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

param = "database"
database = Param()
database.value = params[param]
database.name = param
database.max_length = Constants.POSTGRES_NAMEDATA_LEN
database.require = True
database.sanitizier = "sql"
sanitized_arguement[param] = database.get()


# ******************
# *  SQL SENTENCE  *
# ******************
clean_sql = ("CREATE DATABASE {db};").format(db=sanitized_arguement['database'])
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

# Parse Output
for line in output.split(linesep):
    if ("ERROR:" in line) and (" database " in line) and ("already exists" in line):
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

# Report Output
if exitcode == 0:
    # We good
    print("{status}=ok".format(status=Constants.API_SUMMARY_STRING))
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('DATABASE_ALREADY_EXIST')
    if error_scenario_2:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_3:
        error_hint.append('SQL_ERROR')
    if error_scenario_4:
        error_hint.append('FATAL_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("{status}=rollback".format(status=Constants.API_SUMMARY_STRING))
    print("{errors}={reasons}".format(reasons=error_hint,
        errors=Constants.API_ERROR_STRING))

toolkit.exit(exitcode)