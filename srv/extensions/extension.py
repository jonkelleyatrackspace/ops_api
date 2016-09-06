#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016, Jonathan Kelley
#
# License: the mit license
#    Permission is hereby granted, free of charge, to any person obtaining a copy of
#    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#    the Software, and to permit persons to whom the Software is furnished to do so,
#    subject to the above copyright notice and this permission notice shall being included
#    in all copies or substantial portions of the Software.

from __future__ import print_function
from constants import Constants
import sys

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
    def fail(name="", exitcode=1, error_indicators=[], message="",stdout="",stderr=""):
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
        Session.fail(name,199,['NULL_INPUT_ERROR'],"Unprocessable entity, undefined parameter")



