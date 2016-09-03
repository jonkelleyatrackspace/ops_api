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

# -- jojo --
# description: Reload server configs without restarting
# http_method: get
# lock: False
# tags: Postgres, Psql
# -- jojo --

from os import linesep
from blueprint import CmdRun, ToolKit

# Spawn Instances
run = CmdRun()        # <class> Run
toolkit = ToolKit()  # <class> Misc. functions


# ******************
# *  SQL SENTENCE  *
# ******************
sql = ("BEGIN; select pg_reload_conf(); COMMIT;")
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
error_scenario_3 = False

for line in query_result.split(linesep):
    if (line == "ROLLBACK") or ("transaction is aborted, commands ignored" in line):
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if ("psql:/tmp/" in line) and (" ERROR:  " in line):
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL: " in line:
        toolkit.print_stderr(line)
        error_scenario_3 = True
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
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("return_value execution_status=rollback")
    print("return_value error_reason_indicator={error}".format(
        error=error_hint))

toolkit.exit(exitcode)
