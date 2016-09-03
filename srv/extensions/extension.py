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

from __future__ import print_function      # for print_stderr
from sys import stderr                     # for print_stderr
from os import environ as env              # for paramaters
from os import chmod, chown, unlink        # for tempfile
from tempfile import NamedTemporaryFile    # for tempfile
from pwd import getpwnam                   # for tempfile
from subprocess import Popen, PIPE, STDOUT  # for command runs
from pwd import getpwnam                   # for tempfile
import re as regex                         # for eval sanitize


class CmdRun():
    """
    CLASS: Handles the execution of commands using subprocess.
           run() is the main business end of the class, while subsequent functions
           are primarily made to aid customized command processing.
    """

    def run(self, command):
        """
        Runs a command and returns combined STDERR/STDOUT

        :param command: <STR> command to run
        :return <str>:
        """
        out = Popen(command.split(), stderr=STDOUT, stdout=PIPE, shell=False)
        stdout = out.communicate()[0]
        return stdout

    def sql(self, sql_code):
        """
        Runs a set of SQL code using run(), and returns the run() object back.

        :param sql_code: <STR> SQL query to run
        :return <FUNCTION self.run>:
        """
        sql_shell = "/usr/bin/sudo -u postgres /usr/bin/psql -U postgres -a -f {sql}".format(
            sql=sql_code)
        return self.run(sql_shell)

    def ansible(self, ansible_opts):
        """
        Supports running external ansible-playbook commands.
        Each k,v in a dictionary passed to ansible_opts will be
        added as --k=v to the commandline.
        Special exceptions for playbook and append_args as those
        are not exactly straight up flags.

        :param ansible_opts: <dict> with k,v of options to use
        :return <FUNCTION self.run>:
        """
        args = ""
        for k, v in ansible_opts.iteritems():
            if k == "playbook":
                # If this is the playbook option, work this into the CLI
                args = " {ansible} {opt} ".format(ansible=args, opt=v)
            elif k == "append_args":
                # If this is the playbook option, work this into the CLI
                args = " {ansible} {append_args} ".format(ansible=args, append_args=v)
            elif k == "--extra-vars":
                # Literal quotes extra vars for proper execution
                #  (This may need to be done for other flags)
                args = "{ansible} {arg}='{opt}' ".format(ansible=args, arg=k, opt=v)
            elif k.startswith('-') and v == k:
                # If value matches key then it's a -flag or --flag switch.
                args = "{ansible} {switch} ".format(ansible=args, switch=v)
            elif v != '':
                # If value is not empty, then set the value
                args = "{ansible} {arg}={opt} ".format(ansible=args, arg=k, opt=v)
            else:
                print("Error?")
                exit(1)

        command = ('/usr/bin/ansible-playbook {args}').format(args=args)
        toolkit = ToolKit()
        print("XXXXX")
        print(command)
        proxyscript = ("#!/bin/bash\n\n{cmd}").format(cmd=command)
        sh = toolkit.write_temp(proxyscript)

        exe = "/bin/bash {tmpfname}".format(tmpfname=sh)
        result = self.run(exe)
        toolkit.close()
        return result

    def fabric(self, fab_opts):
        """
        UNTESTED AT THE MOMENT (NO PROOF OF CONCEPT)
        Support running external fabric scripts.
        Each k,v in a dictionary passed to fab_opts will be added as
        a --k=v to the commandline for ansible.
        Special exception is made for 'command' as that's not a flag, but
        the main argv1.

        :param fab_opts: <dict> with k,v of options to use
        :return <FUNCTION self.run>:
        """
        args = ""
        for k, v in ansible_opts.iteritems():
            if k == "fabricargs":
                # If value is fabric command, set this up
                args = " {fab} {arg1} ".format(fab=fabcmd, arg1=v)
            elif k.startswith('-') and v == k:
                # If value matches key then it's a -flag or --flag switch.
                args = "{fab} {switch} ".format(fab=fabcmd, switch=v)
            elif v != '':
                # If value is not empty, then set the value
                args = "{fab} {arg}={opt} ".format(fab=args, arg=k, opt=v)
            else:
                print("Error?")
                exit(1)

        command = ('/usr/local/bin/fab {args}').format(args=args)
        toolkit = ToolKit()
        proxyscript = ("#!/bin/bash\n\n{cmd}").format(cmd=command)
        sh = toolkit.write_temp(proxyscript)

        exe = "/bin/bash {tmpfname}".format(tmpfname=sh)
        result = self.run(exe)
        toolkit.close()
        return result

    def web(self, x):
        """
        """
        # Call requests handler class. TODO rax identity class.
        return False


class Constants():
    """
    CLASS: Fixed properties that rarely change
    """
    LINUX_MAX_FILE_NAME_LENGTH = 255
    LINUX_MAX_FILE_PATH_LENGTH = 4096

    # These are the api status output keys
    API_RETURN_STRING = "return_value"
    API_SUMMARY_STRING = "{v} status".format(v=API_RETURN_STRING)
    API_ERROR_STRING = "{v} errors".format(v=API_RETURN_STRING)

    # Postgres uses  no more than  NAMEDATALEN-1 bytes
    # of an  identifier;  longer names can be written in
    # commands, but they will be truncated.  By default,
    # NAMEDATALEN is 64 so the maximum identifier length
    # is 63 bytes.
    POSTGRES_NAMEDATA_LEN = 64

    # User selectable socket limits can go this high
    POSTGRES_CONNECTION_LIMIT = 25

    # Busted user selectable socket limits can go this high
    # We don't need to get sockets too high.
    POSTGRES_MAXIMUM_CONNECTION_LIMIT = 150


class Environment():
    """
    CLASS: Manages environment properties.
    # THIS CLASS WILL GO AWAY WITH PARAM2 
    """

    def params(self):
        """
        Returns json params from parent environment

        """
        params = {}
        for param, value in env.iteritems():
            params[param] = value
        params = dict((k.lower(), v) for k,v in params.iteritems())
        return params


class SecurityFaultInvalidFileAccessAttemp(Exception):
    """ This will be raised if somehow a non-tmp file is attempted to be written to.
        This should require tmp in the file path or name severely limiting access scope.
    """
    def __init___(self,dErrorArguments):
        Exception.__init__(self,"{0}".format(dErrArguments))
        self.dErrorArguments = dErrorArguements


class ToolKit():
    """
    CLASS: Misc. functions
    """

    def print_stderr(self, *args, **kwargs):
        """
        Prints a message to stderr.
        Requires sys.stderr

        """
        print(*args, file=stderr, **kwargs)

    def fail_beyond_maxlength(self, maxlength=0, string=""):
        """
        If a string is beyond a certain length, fail.
        Long inputs are indicative of fuzzing in some instances.
        It's a security bailout
        """
        if len(string) > maxlength:
            print("{return_macro} status=rollback".format(return_macro=Constants.API_RETURN_STRING))
            print("{return_macro} troubleshoot=UNKNOWN".format(return_macro=Constants.API_RETURN_STRING))
            exit(1)

    def harden_permissions(self, fname):
        """
        Sets permissions on the tmpfiles for reasonable security.
        """
        #uid = getpwnam('postgres').pw_uid
        #gid = getpwnam('postgres').pw_gid
        chmod(fname, 0777)      # o+rw
        # chown(fname, uid, gid)  # chown postgres: fname

    def write_to_file(self, filepath, text=""):
        """
        Writes text to a tmp file, used to update tmp files

        :return f.name: the name of the file written to
        """
        if "/tmp/tmp" not in filepath:
            raise SecurityFaultInvalidFileAccessAttempt(filepath)
        with open(filepath, "w") as f:
            f.write("{text}".format(
                text=text))
            return f.name

    def write_temp(self, content):
        """
        Write intermediary contents to a temporary file handle.
        :param content: The content you wish to save

        :return f.name: the name of the file.
        """
        with NamedTemporaryFile(mode='w+b', delete=False) as f:
            self.f = f.name
            f.write(content)  # Write
            self.harden_permissions(f.name)
            return f.name

    def exit(self,value=0):
        """
        Exits the application, unlinks write_temp resouce from /tmp

        :param value: exit value

        :return: exit(value)
        """
        unlink(self.f)
        return exit(value)

    def close(self,value=0):
        """
        Just close, no esit

        :param value: returns

        :return: exit(value)
        """
        unlink(self.f)
        return value

class Sanitize():
    """
    CLASS:  String sanitization functions for safe eval
            You put a string in, get  a string out.
    """

    def __init__(self):
        self.err = ToolKit()

    def terminate_suspicious_input(self, testtext):
        """
        At least every Sanitize() method should run the data through here
        before passing subprocess. This routine is specialized to detect
        the patterns of escapes seen by pipes.quote (shlex.quote in Python 3)
        when doing various types of control character injection.

        If one pair (or more) of escape sequences is detected
        this request will fail.
        """
        # This will count the number of escape sequences attempted and then 
        #  promplty throw an exception.
        # TODO Audit logging for this sort of event?
        begin_escape_seqs = len(tuple(regex.finditer(r"''\"'\"'", testtext)))
        end_escape_seqs = len(tuple(regex.finditer(r"'\"'\"''", testtext)))
        escape_sequences_count = begin_escape_seqs + end_escape_seqs
        if escape_sequences_count > 0:
            # We're getting escape sequences
            #  This user may be fuzzing the API so 
            #   quietly exit stage right
            #    -->
            print("{return_macro} status=500".format(return_macro=Constants.API_RETURN_STRING))
            print("{return_macro} message=Framework encountered an internal error".format(
                return_macro=Constants.API_RETURN_STRING))
            self.err.print_stderr("An internal error has occurred.")
            exit(254)
        else:
            return 0

    def non_alphanumeric_text(self, varied_input):
        """
        Should return a string safe to run anywhere, considering
        it's only alpha-numeric text.

        :param your_string: The string you wish to escape.
        """
        self.terminate_suspicious_input(varied_input)
        return regex.sub(r'\W+', '', varied_input)

    def sql(self, sql):
        """
        Place holder for SQL sanitizer. This is well handled by the 
        pipes.quote / shlex.quote library it seems and the tamper detection.
        """
        fail = 0
        errmessage = ""
        self.terminate_suspicious_input(sql)

        if len(tuple(regex.finditer(r"%", sql))):
            fail = 240
            errmessage = "Forbidden characters found in input data"

        if fail > 0:
            print("{return_macro} status=400".format(return_macro=Constants.API_RETURN_STRING))
            self.err.print_stderr(errmessage)
            exit(fail)

        return sql

class ParamHandle():
    """
    CLASS: Parameter handling. This class does a multitude of things,
           including getting the parameters from the environment() class,
           as well as helping with params, such as ensuring required 
           env params exist, or that they are not '' (nil)
    """
    name = ""        # Key name of the param  EXAMPLE: "database_host"
    value = ""        # Value of the parameter EXAMPLE: "8.8.8.8"
    max_length = -1        # Maximum len() for value without erroring (-1 is infinite)
    require = False     # Generate API error(s) if value is not supplied.
    sanitizer = None      # Set to the string sanitizer used before returning the
    # use input. Can be None, 'sql', 'nonalphanumeric'
    UTF_00AC = unichr(172) * 4  # DEFINE UTF-8 character U+00AC NOT SIGN
    isbool = UTF_00AC  # Special marker to determine if isbool is used.
    # Valid states are True, False, None so I am using
    # UTF-8 character as a 4th default state.
    default_value = False  # If this property is set, auto-return this value if the
    # user neglects to define this parameter.

    def __init__(self):
        self.err = ToolKit()

    def list(self):
        """
        This will return a dictionary of environment variables.
        It will first pass the strings through a sanitizer, which if 
        given the correct options will sanitize the string.
        """

        env = Environment()  # Instance the shell environment class
        return env.params()

    def get(self):
        """
        This will return a dictionary of environment variables.
        It will first pass the strings through a sanitizer, which if 
        given the correct options will sanitize the string.
        """

        if self.value == "":
            self.raise_error(keyname=self.name, value=self.value,
                             expected_msg="ARG CLASS MISSING VALUE")
        if self.name == "":
            self.raise_error(keyname=self.name, value=self.value,
                             expected_msg="ARG CLASS MISSING NAME")
        if self.require:
            self.fail_if_nil(self.name, self.value)
        if self.max_length > 1:
            if len(self.value) > self.max_length:
                msg = "input less than {max} bytes".format(max=self.max_length)
                self.raise_error(keyname=self.name,
                                 value='too large', expected_msg=msg,
                                 error_reason_indi="BUFFER_OUT_OF_SPACE")

        # Check for overrides that will return a default value if the input is
        # nil.
        if self.default_value:
            if self.is_nil(self.value):
                return self.default_value

        # Check for overrides that convert the return into a boolean or custom
        # value.
        if self.isbool != self.UTF_00AC:
            # We can't use False or None since those might be used
            #  by the user.
            return self.isbool

        # Normal returns, sanitize (if defined) and return the parameter.
        sanitize = Sanitize()
        if not self.sanitizer:
            sanitizedparam = self.value
        elif self.sanitizer == "sql":
            sanitizedparam = Sanitize.sql(self.value)
        elif self.sanitizer == "nonalphanumeric":
            sanitizedparam = Sanitize.non_alphanumeric_text(self.value)

        return sanitizedparam

    def is_nil(self, param):
        """
        Returns true/false depending on if the user
        provided this parameter with a value to the API or not.
        Useful for boolean/value checks.
        An empty parameter is seen as ''"'"''"'"''

        If you think the context is strange, consider
        that export x='"'"''"'"' is basically x="''"
        Which is the escapes occuring at higher abstraction.

        :param param: Input parameter from environ()
        :return: <BOOL>
        """

        # if param == "\\'\\'\\\"\\'\\\"\\'\\'\\\"\\'\\\"\\'\\'":
        #\\'\\'\\\"\\'\\\"\\'\\'\\\"\\'\\\"\\'\\'
        if param == """''\"'\"''\"'\"''""":
            return True
        else:
            return False

    def fail_if_nil(self, keyname, value):
        """
        Causes an error message then exits, used when a parameter is nil.
        """
        if self.is_nil(value):
            print("{return_macro} troubleshoot=UNDEFINED_INPUT_ERROR".format(return_macro=Constants.API_RETURN_STRING))
            self.err.print_stderr(
                "Parameter `{name}` provided with value: <NULL> which cannot be undefined".format(name=keyname))
            exit(500)

    def raise_error(self, keyname, value, expected_msg, error_reason_indi="UNEXPECTED_PARAMETER_INPUT"):
        """
        Causes an error message then exits, used when a parameter is invalid.
        """
        print("{return_macro} troubleshoot={indicator}".format(return_macro=Constants.API_RETURN_STRING,indicator=error_reason_indi))
        self.err.print_stderr("Parameter `{key}` provided with value: {param}, expected: {expect} value.".format(
            key=keyname, expect=expected_msg, param=value))
        exit(500)

    def set_value_if_defined(self, custom_if_value=True, custom_else_value=False):
        """
        Returns return_if value is defined. Else returns return_else.
        Used for parameter processing.
        """
        if not self.is_nil(self.value):
            self.isbool = custom_if_value
        else:
            self.isbool = custom_else_value

    def set_value_if_undefined(self, custom_if_value=True, custom_else_value=False):
        """
        Returns custom_if_value if input is nil. Else returns custom_else_value.
        Used for parameter processing.

        returns True if defined, False if not
        """
        if self.is_nil(self.value):
            self.isbool = custom_if_value
        else:
            self.isbool = custom_else_value

    def convert_to_bool(self, custom_whentrue_value=True, custom_whenfalse_value=False, custom_badinput_value=False):
        """
        Returns as a boolean True if a string approximates a true, and
        a boolean False if a string approximates a false.
        custom_badinput_value returns if it is neither true nor False.
        Used for parameter processing.

        returns True if a string is like a boolean true, False if not
        """
        if self.value.lower().startswith('t') or self.value == "1" or self.value.lower().startswith('y'):
            self.isbool = custom_whentrue_value
        elif self.value.lower().startswith('f') or self.value == "0" or self.value.lower().startswith('n'):
            self.isbool = custom_whenfalse_value
        else:
            self.isbool = custom_badinput_value

if __name__ == "__main__":
    exit(1)
