#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
# License Apache Commons v2
# -- jojo --
# description: Retrieve a list of roles.
# http_method: get
# lock: False
# tags: Postgres, Psql
# -- jojo --

from os import linesep
from blueprint import CmdRun, ToolKit

# Spawn Instances
run = CmdRun()   # <class> Run
toolkit = ToolKit()  # <class> Misc. functions


# ******************
# *  SQL SENTENCE  *
# ******************
sql = ("\du")
sql_code = toolkit.write_temp(sql)


# ****************
# *  SQL RUNNER  *
# ****************
output = run.sql(sql_code)
print(output)
print("jojo_return_value execution_status=ok")

toolkit.exit(0)
