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
# description: Retrieve a list of roles.
# http_method: get
# lock: False
# tags: Postgres, Psql
# -- config --

from os import linesep
from extension import CmdRun, ToolKit, Constants

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
print("{status}=ok".format(status=Constants.API_SUMMARY_STRING))

toolkit.exit(0)
