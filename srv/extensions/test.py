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
# description: This config block will go away soon since class properties encode this now.....
# param: name - Your name
# param: age - Your age
# http_method: post
# lock: False
# -- end config --

from __future__ import (print_function, absolute_import)
import datetime

from constants import Constants as constants
from constants import HttpMethod as method
from param import (ParameterCollection, BaseParameter, get_parameter, validate_parameters)
from param import Convert as convert
from param import (Session, BaseExtension)



dt = datetime.datetime.now()
parameter = ParameterCollection()


# *************************
# * User Input Parameters *
# *************************
@parameter.define
class name(BaseParameter):
  __doc__ = "Input your first name"
  name = "name"
  max_length = 128
  censor_logs = False

  def input_validation(self,user_input):
    # die if parameter JSON missing in request
    self.fail_if_null(
      parameter=self.name,
      value=user_input)
    # die if any of these "bad" characters get procesed
    self.disallow_characters(
      parameter=self.name,
      badlist=['-', '.'],
      value=user_input)

@parameter.define
class age(BaseParameter):
  __doc__ = "Input how old you are (in years)"
  name = "age"
  max_len = 3
  max_int = 99
  censor_logs = False

  def input_validation(self,user_input):
    # die if parameter JSON missing in request
    self.fail_if_null(
      parameter=self.name,
      value=user_input)

# Don't forget this! o.O
import timeit
validate_parameters(parameter)



# *************************
# * Define Business Logic *
# *************************
class test(BaseExtension):
  __doc__ = "Demo extension for v2 SDK, take your name & age and print your birth year"
  uuid = "b0b934fd-d978-4bd8-b194-1cd4a3f5166b" # unique identifier for extension
  http_method = method.post # the http request verb this extension can be
  lock = False # if True, only 1 execution at a time can run
  tags = ['example_1', 'test_tag', 'try_me'] # tag this extension

  def __init__(self):
    BaseExtension.__init__(self) # base __init__

  def run(self):
    """
    So everything is ready to go. Do your logic and return!!
    You can reference any parameter defined above with 
    get_parameter(parameter, NAME); where NAME is your parameter name.

    """
    birthyear =  dt.year - int(get_parameter(parameter, 'age'))

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
      age=get_parameter(parameter, 'age'),
      whom=get_parameter(parameter, 'name'),
      u=get_parameter(parameter, 'name').title(),
      year=birthyear,
      datetime=dt))
    Session.close(0)


# *****************
# * Start Request *
# *****************
if __name__ == "__main__":
  me = test()
  test.run(me)

