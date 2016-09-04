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
# description: Identify slow queries
# http_method: get
# lock: False
# tags: Postgres, Psql
# -- end config --

from os import linesep
from extension import CmdRun, ToolKit, Constants

# Spawn Instances
run = CmdRun()        # <class> Run
toolkit = ToolKit()  # <class> Misc. functions


# ******************
# *  SQL SENTENCE  *
# ******************
sql = ("SELECT"
       "    pid,"
       "    current_timestamp - xact_start as xact_runtime,"
       "    query"
       " FROM pg_stat_activity WHERE query NOT LIKE '%pg_stat_activity%' "
       " ORDER BY xact_start;"
       )
sql_code = toolkit.write_temp(sql)


# ****************
# *  SQL RUNNER  *
# ****************
query_result = run.sql(sql_code)


# **********************
# *  OUTPUT PROCESSOR  *
# **********************
print(query_result)
exitcode = 0  # We good
error_scenario_1 = False
error_scenario_2 = False

for line in query_result.split(linesep):
    if ("psql:/tmp/" in line) and (" ERROR:  " in line):
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL: " in line:
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.

# Report Output
if exitcode == 0:
    # We good
    print("{status}=ok".format(status=Constants.API_SUMMARY_STRING))
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('SQL_ERROR')
    if error_scenario_2:
        error_hint.append('FATAL_ERROR')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("{status}=rollback".format(status=Constants.API_SUMMARY_STRING))
    print("{errors}={reasons}".format(reasons=error_hint,
        errors=Constants.API_ERROR_STRING))

toolkit.exit(exitcode)
