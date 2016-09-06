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

from constants import Constants as constants
from param import ParameterCollection, BaseParameter, get_parameter, validate_parameters
from param import Convert as convert
from extension import EndSession, Extension

import datetime


# *************************
# * Define Local Instance *
# *************************
dt = datetime.datetime.now()
parameter = ParameterCollection()


# *************************
# * Define Request Params *
# *************************
@parameter.define
class name(BaseParameter):
  __doc__ = "Input your first name"
  name = "name"
  max_length = 128
  censor_logs = False
  def evalulate_parameter(self,parameter_input):
    self.fail_if_null(self.name, parameter_input)

@parameter.define
class age(BaseParameter):
  __doc__ = "Input how old you are (in years)"
  name = "age"
  max_len = 3
  max_int = 99
  censor_logs = False
  def evalulate_parameter(self,parameter_input):
    self.fail_if_null(self.name, parameter_input)


# *********************************
# * Fail if params fail vaidation *
# *********************************
validate_parameters(parameter)


# *********************************
# * Define Request Business Logic *
# *********************************
class test(Extension):
  def __init__(self):
    Extension.__init__(self)

  def run(self):
    """
    Define the code for this extension.
    Parameters provided defined above are built by using
       get_parameter(parameter)['age']['value']

    """
    birthyear =  dt.year - int(get_parameter(parameter)['age']['value'])

    # *************
    # *  RESULTS  *
    # *************
    print((
        "{status} current_datetime={datetime}\n"
        "{status} name={whom}\n"
        "{status} age={age}\n"
        "{status} status={u} was born in {year}"
        ).format(
        status=constants.API_RETURN_STRING,
        age=get_parameter(parameter)['age']['value'],
        whom=get_parameter(parameter)['name']['value'],
        u=get_parameter(parameter)['name']['value'].title(),
        year=birthyear,
        datetime=dt))
    EndSession.close(0)


# *************
# * Run Logic *
# *************
if __name__ == "__main__":
  me = test()
  test.run(me)

