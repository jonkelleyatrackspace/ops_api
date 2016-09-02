#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: Retrieve pg stats connection activity (whos connected)
# http_method: get
# lock: False
# tags: Postgres, PGaaS, cit-ops
# -- jojo --

from blueprint import ToolKit, CmdRun

# Spawn Instances
toolkit = ToolKit()
run = CmdRun()        # <class> Run


# ******************
# *  SQL SENTENCE  *
# ******************
sql = ("BEGIN; select * from pg_stat_activity; COMMIT;")
sql_code = toolkit.write_temp(sql)

# ****************
# *  SQL RUNNER  *
# ****************
output = run.sql(sql_code)


# **********************
# *  OUTPUT PROCESSOR  *
# **********************
print(output)
print("return_value execution_status=ok")
toolkit.exit()