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

from __future__ import absolute_import

class Constants():
    """
    These are constants you may want to reference in your local modules.
    """
    LINUX_MAX_FILE_NAME_LENGTH = 255
    LINUX_MAX_FILE_PATH_LENGTH = 4096

    # These are the api status output keys
    API_RETURN_STRING = "return_value"
    API_SUMMARY_STRING = "{v} result".format(v=API_RETURN_STRING)
    API_ERROR_STRING = "{v} troubleshoot".format(v=API_RETURN_STRING)

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

class HttpMethod():
    """
    defines common http methods from rfc2616
    """
    options = "OPTIONS"
    get = "GET"
    head = "HEAD"
    post = "POST"
    put = "PUT"
    delete = "DELETE"
    trace = "TRACE"
    connect = "CONNECT"