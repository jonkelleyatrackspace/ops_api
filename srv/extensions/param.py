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

from extensionSdk import EndSession
from os import environ
import inspect # used by compile_parameters()


def validate_parameters(cls_collection):
    """
    this will scope through the registered Parameter class children
    and generate a dictionary object with parameter properties out of it.

    The cls_collection arguement should be a class instance of
      ParameterCollection()

    this introduced so the parent OPSAPI app can "query" parameters out of
    extension modules programatically. might come in handy for more.

    :return <DICT> -- dict with keys of each parameter title,
                      the value is a dict with k,v pairs of class
                      properties.
    """
    params = get_parameter(cls_collection).iteritems()
    for cls,clsmembers in params:
        for class_member, value in clsmembers.iteritems():
            if class_member == "__self__":
                # We found the reference to its own class object
                # run the evaluate function on it.
                value.evalulate_parameter(clsmembers['value'])

def get_parameter(cls_collection):
    """
    this will scope through the registered Parameter class children
    and generate a dictionary object with parameter properties out of it.

    The cls_collection arguement should be a class instance of
      ParameterCollection()

    this introduced so the parent OPSAPI app can "query" parameters out of
    extension modules programatically. might come in handy for more.

    :return <DICT> -- dict with keys of each parameter title,
                      the value is a dict with k,v pairs of class
                      properties.
    """
    param_map = {}
    for cls_title,cls_obj in cls_collection.collection.iteritems():
      try:
        real_cls_title = cls_obj.name
        # Prefer to use cls.name member to the actual class name.
      except AttributeError:
        # No cls.name DEFINED, lets use the actual class name.
        real_cls_title = cls_title
      param_map[real_cls_title] = {}
      class_members = inspect.getmembers(cls_obj, ## import inspect
        lambda a:not(
          inspect.isroutine(a)
          )
        )
      for class_member in class_members:
        member, v = class_member
        if member == "__module__":
          pass # nobody needs __module:__main
        else:
          param_map[real_cls_title][member] = v

      if param_map[real_cls_title]['value']: # value override set!!!!
        # The user has set the value for us, lets use the classmember instead of shellenv.
        param_map[real_cls_title][member] = param_map[real_cls_title]['value']
      else:
        # Use the shell env
        env = ShellEnv.get()
        try:
            param_map[real_cls_title][member] = env[real_cls_title]
        except:
            pass
      param_map[real_cls_title]['__self__'] = cls_obj
    return param_map

class ShellEnv():
    """
    This will fetch the environment variables from the parent environment.
    This is how the parent API passes data into params in the framework.
    """

    @staticmethod
    def get():
        """
        Returns json params from parent environment

        """
        shellvars = {}
        for var, val in environ.iteritems():
            shellvars[var] = val
        shellvars = dict((k.lower(), v) for k,v in shellvars.iteritems())
        return shellvars

class ParameterCollection():
    """
    This will let you register a collection of classes into
    a collection by tag of the @define decorator.

    Simply instanciate with i = ParameterPool() and then
    decorate classes with @define and they will be stored
    in the collection class member.

    You can reference and call these classes now, yay.
    """
    collection = {}
    def define(self,cls):
        """ This is used as a decorator """
        name = cls.__name__
        force_bound = False
        if '__init__' in cls.__dict__:
            cls.__init__.func_globals[name] = cls
            force_bound = True
        try:
            self.collection[name] = cls()
        finally:
            if force_bound:
                del cls.__init__.func_globals[name]
        return cls

class Convert():
    """
    This will convert parameter types to other types
    """
    @staticmethod
    def to_bool(value, booltrue_override=True, boolfalse_ovverride=False, notabool_override=None):
        """
        This will convert a vaue into a boolean.
        If a string represents 'true' then cast to True
        If a string representse 'false' then cast to False
        If a string is non-deterministic then cast to None

        Override these with the method params
        """
        if value.lower().startswith('t' )or value == "1" or value.lower().startswith('y'):
            return booltrue_override
        elif value.lower().startswith('f') or value == "0" or value.lower().startswith('n'):
            return boolfalse_ovverride
        else:
            return value
    def to_int(value):
        """
        Converts a string to an integer
        """
        return int(value)

class BaseParameter():
    """
    This defines a single parameter object in an extension.

    This will define the attributes for each parameter, and is used
    for parameter validation when it's time.

    This class sets the base attributes.
    """
    nullvalue = """''\"'\"''\"'\"''""" # what a null value from the frontend will be
    max_len = -1 # used to validate user input len, fail request if above this
    max_int = -1 # use to vaidate user input, ensure <int> and not greater then this
    value = None # gets set by build_parameter
    censor_logging = False

    # Mock empty in the event of discovery functions.
    def __call__(self):
        pass

    def evalulate_parameter(self,parameter_input_from_userland):
        """
        Evaluator.
        This can be redefined to call assertion functions
        on each parameter. This method is called when a request
        is made to ensure the parameter input meets the authors intentions.
        """
        return False

    def fail_if_null(self,parameter,value):
        """
        Asserter.
        Exit if parameter is null.
        """
        if self.is_null(value):
            EndSession.fail_null_parameter(name=self.name)
        else:
            pass

    def is_null(self,value):
        """
        Helper.
        True if parameter is null.
        """
        if value == self.nullvalue or value == None:
            return True
        else:
            return False

    def is_defined(self,value):
        """
        Helper.
        True if parameter is defined with some value (not null).
        """
        if value != self.nullvalue:
            return True
        else:
            return False