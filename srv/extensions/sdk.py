#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: sdk.py
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

from __future__ import (print_function, absolute_import)
from os import environ
import inspect # used by compile_parameters()
import sys

from constants import Constants

"""
This is the Source Development Kit (SDK) for OpsAPI
https://github.com/jonkelleyatrackspace/ops_api

This can be imported from within the namespace of extension modules, and is used by the
CORE extensions available to opsapi. You can utilize this SDK in your own extensions
by accessing classes, functions and methods. Private methods/functions will start with
an underscore, and should NOT be called (they may change between "official" versions.
"""
 
# This SDK is subject to change. If you modify a public function, classname or method
# then look at what you should mark this change as below.
# - New Classes/Methods           = Minor Release
# - Rename/Delete Classes/Methods = Major Release
# The Tornado app will build a collection of extensions and check sdk compatability
# against the version below. If the version is not compatible then the extension
# will be excluded from the import into OPSAPI and a log message generated.
#
# Extensions will be able to use > < macros in their definitions to take advantage
# of known specifics. Format is SDK_VERSION = "M.m" (M=major,m=minor)
SDK_VERSION = "2.0"

def validate_parameters(cls_collection):
    """
    this will scope through the registered Parameter class children
    and generate a dictionary object with parameter properties out of it.

    The cls_collection arguement should be a class instance of
      ParameterCollection()

    this introduced so the parent OPSAPI app can "query" parameters out of
    extension modules programatically. might come in handy for more.

    """
    params = get_parameter(cls_collection).iteritems()
    for cls,clsmembers in params:
        for class_member, value in clsmembers.iteritems():
            if class_member == "__self__":
                # We found the reference to its own class object
                # run the evaluate function on it.
                value.input_validation(clsmembers['value'])

def get_parameter(cls_collection,parameter=None,member='value'):
    """
    This will iterate through each parameter in the collection.
    It takes all the class members and then generated parameter properties
    out of the parameter class with it.

    cls_collection is a class instance of ParameterCollection()

    If you wish to retrieve the member name of a particular parameter,
    simply define parameter, and define member as the member key you want.
    By default it pulls parameter value.

    -- Params --
    parameter -- This will look for a member within this parameter class obj.
    member -- This returns the value of this member item. 

    -- Return --
    It returns a dict with member keys from each parameter class.
    Each parameter class has k,v pairs for its member(s)
    <DICT>
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
    if parameter:
        # filter by parameter
        return param_map[parameter]['value']
    else:
        # Return all parameters in map
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

    def input_validation(self,user_input):
        """
        Evaluator.
        Redefine this as you need to validate the parameter's user_input
        on execution. You can set the self.value property at your own
        discretion. Primarily used to QUIT when bad inputs caught.
        """
        # self.value = "new value"
        return


    def disallow_characters(self,parameter, badlist ,value):
        """
        Asserter.
        If we find any of the bad characters, fail. Useful for input management.
        """
        for c in badlist:
            if c in value:
                Session.fail_badchar_parameter(name=self.name)

    def fail_if_null(self,parameter,value):
        """
        Asserter.
        Exit if parameter is null.
        """
        if self.is_null(value):
            Session.fail_null_parameter(name=self.name)
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


def print_stderr(*args, **kwargs):
    """
    Prints a message to stderr.
    Requires sys.stderr

    """
    print(*args, file=sys.stderr, **kwargs)

class BaseExtension():
    """
    This defines a single extension within the framework.
    """
    def __init__(self):
        #keeps track of the scripts output
        self._outputData = []
        self.trigger = 'call'
        #used to stop any loops you may have
        self._running = True

    def build_extension_id(self,uuid):
        self.uuid = "".join(uuid.split("-"))
        return

    def _output(self, data):
        self._outputData.append(data)

    def get_output(self):
        return self._outputData

    def stop(self):
        self._running = False

class Session():
    """
    This is used for handling exiting the request framework in a handled manner.
    """
    @staticmethod
    def exit(code=0):
        """
        Just exit. Not typically called by itself.
        """
        exit(code)

    @staticmethod
    def close(exitcode):
        """
        Just exit. Not typically called by itself.
        """
        exit(exitcode)

    @staticmethod
    def fail(name="", exitcode=1, error_indicators=[], message="",stdout=None,stderr=None):
        """
        Used to trigger a fail message.
        """
        print("{return_macro} parameter='{param}'".format(param=name, return_macro=Constants.API_RETURN_STRING))
        print("{return_macro} statusMsg='{message}'".format(message=message, return_macro=Constants.API_RETURN_STRING))
        print("{return_macro} status={exitcode}".format(exitcode=exitcode, return_macro=Constants.API_RETURN_STRING))
        print("{return_macro} troubleshoot={error_indicators}".format(error_indicators=error_indicators, return_macro=Constants.API_RETURN_STRING))
        print_stderr(stderr)
        print(stdout)
        exit(exitcode)

    @staticmethod
    def fail_null_parameter(name=""):
        """
        Template for erroring when input is NULL
        """
        Session.fail(name,exitcode=199,
            error_indicators=['NULL_INPUT_ERROR'],
            message="Unprocessable entity, undefined parameter")

    @staticmethod
    def fail_badchar_parameter(name=""):
        """
        Template for erroring when input has bad input characters
        """
        Session.fail(name,exitcode=198,
            error_indicators=['INPUT_CONTAINS_INVAL_DATA'],
            message="Unprocessable entity, parameter contains invalid character")
