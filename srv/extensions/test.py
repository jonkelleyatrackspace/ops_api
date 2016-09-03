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
# description: A test file to validate functionality and get up and running
# param: name - Your name
# param: age - Your age
# http_method: post
# lock: False
# -- config --

from extension import Constants
from extension import ParamHandle as Param
import datetime

# Spawn Instances
p = Param()    # <class> Parame ter manipulation
params = p.list()    # <dict>  A dict of params
dt = datetime.datetime.now()  #<datetime> object

# ************************************
# *  DEFINE PARAMETERS AND VALIDATE  *
# ************************************
arguement = {} # The actual API params we pass

param = "name"
name = Param()
name.value = params[param]
name.name = param
name.require = True
name.max_length = 128
arguement[param] = name.get()


param = "age"
age = Param()
age.value = params[param]
age.name = param
age.require = True
age.max_length = 3
age.max_int = 99
arguement[param] = age.get()
# Calculate cake day
birthyear =  dt.year - int(arguement['age'])


# *************
# *  RESULTS  *
# *************
print(("{status} current_datetime={datetime}\n"
  "{status} name={whom}\n"
  "{status} age={age}\n"
  "{status} status=You were born in {year}").format(
  status=Constants.API_RETURN_STRING,
  age=arguement['age'],
  whom=arguement['name'],
  year=birthyear,
  datetime=dt))

exit(0)
