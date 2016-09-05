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
# -- end config --

from extension import Constants, Extension
from extension import Parameter
from extension import ParamHandle as Param
import datetime

# Spawn Instances
parent_params = Param()
parent_param = parent_params.list() # Get dict of params
dt = datetime.datetime.now() #<datetime> object

def parameter(ok):
  """ Dummy function for validation """
  return ok

registry = {}
def register_parameter(cls):
    name = cls.__name__
    force_bound = False
    if '__init__' in cls.__dict__:
        cls.__init__.func_globals[name] = cls
        force_bound = True
    try:
        registry[name] = cls()
    finally:
        if force_bound:
            del cls.__init__.func_globals[name]
    return cls

@register_parameter
class name(Parameter):
    name = "name"
    value = parent_param[name]
    __doc__ = "Your name"
    error_if_undefined = True
    max_length = 128
    censor_log = False

@register_parameter
class age(Parameter):
    name = "age"
    value = parent_param[name]
    __doc__ = "Your age"
    error_if_undefined = True
    max_len = 3
    max_int = 99
    censor_log = False

class test(Extension):
    def __init__(self):
        Extension.__init__(self)

    def run(self):
        #Your code here...
        print("IT works!")
        birthyear =  dt.year - int(arguement['age'])

        # *************
        # *  RESULTS  *
        # *************
        print(("{status} current_datetime={datetime}\n"
          "{status} name={whom}\n"
          "{status} age={age}\n"
          "{status} status={u} was born in {year}").format(
          status=Constants.API_RETURN_STRING,
          age=arguement['age'],
          whom=arguement['name'],
          u=arguement['name'].title(),
          year=birthyear,
          datetime=dt))

def return_parameters():
    """ Will return a dictionaries, key of the parameter
    name and """
    x = {}
    for parameter,cls in registry.iteritems():
      x[cls.name] = {}
      cls.value = parent_param[cls.name] # Set the value from ENV
      x[cls.name]['value'] = cls.value
      x[cls.name]['censor_log'] = cls.censor_log

    return x

print(return_parameters())

exit(0)
