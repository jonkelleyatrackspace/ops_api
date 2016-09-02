#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: Retrieve pg_is_in_recovery() status
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
sql = ("\\x on\n SELECT pg_is_in_recovery();")
sql_code = toolkit.write_temp(sql)


# ****************
# *  SQL RUNNER  *
# ****************
output = run.sql(sql_code)


# **********************
# *  OUTPUT PROCESSOR  *
# **********************
print(output)
exitcode = 0  # We good
error_scenario_1 = False
error_scenario_2 = False
error_scenario_3 = False
pg_is_in_recovery = None

for line in output.split(linesep):
    if (line == "ROLLBACK") or ("transaction is aborted, commands ignored" in line):
        toolkit.print_stderr(line)
        error_scenario_1 = True
        exitcode = 1  # Rollbacks should flag an API error code.
    if ("psql:/tmp/" in line) and (" ERROR:  " in line):
        toolkit.print_stderr(line)
        error_scenario_2 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if " FATAL:  " in line:
        toolkit.print_stderr(line)
        error_scenario_3 = True
        exitcode = 1  # Parse Errors should flag an API error code.
    if "pg_is_in_recovery | t" in line:
        pg_is_in_recovery = "true"
        server_class = "REPLICA"
        exitcode = 0  # We good
    if "pg_is_in_recovery | f" in line:
        pg_is_in_recovery = "false"
        server_class = "MASTER"
        exitcode = 0  # We good

if not "pg_is_in_recovery | " in output:
    error_scenario_99 = True
    exitcode = 1  # Something strange happened

if exitcode > 0:
    pg_is_in_recovery = "none"
    server_class = "UNKNOWN_RECOVERY_STATUS"

# Report Output
if exitcode == 0:
    # We good
    print("return_value server_type={server_class}".format(
        server_class=server_class))
    print("return_value pg_is_in_recovery={status}".format(
        status=pg_is_in_recovery))
    print("return_value execution_status=ok")
else:
    # Errors should flag an API error code.
    error_hint = []
    if error_scenario_1:
        error_hint.append('TRANSACTION_ROLLBACK')
    if error_scenario_2:
        error_hint.append('SQL_ERROR')
    if error_scenario_3:
        error_hint.append('FATAL_ERROR')
    if error_scenario_99:
        error_hint.append('CANNOT_DETERMINE_REPLICATION_STATUS')
    if len(error_hint) == 0:
        error_hint = ['UNKNOWN']
    print("return_value server_type={server_class}".format(
        server_class=server_class))
    print("return_value pg_is_in_recovery={status}".format(
        status=pg_is_in_recovery))
    print("return_value execution_status=rollback")
    print("return_value error_reason_indicator={error}".format(
        error=error_hint))

toolkit.exit(exitcode)
