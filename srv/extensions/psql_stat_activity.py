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
# description: Retrieve pg stats connection activity (whos connected)
# http_method: get
# lock: False
# tags: Postgres, PGaaS, cit-ops
# -- end config --

from extension import ToolKit, CmdRun, Constants

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
print("{status}=ok".format(status=Constants.API_SUMMARY_STRING))

toolkit.exit()
