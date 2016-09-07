#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: constants.py
# ---
# © 2016, Jonathan Kelley <jon@uberleet.org>
# Underwritten by The MIT License:
#    Permission is hereby granted,  free of charge,  to any person obtaining 
#    a copy of this software and associated documentation files  (the "Soft-
#    ware"), to deal in the Software without restriction,  including without
#    limitation the rights to use,  copy, modify, merge, publish, distribute
#    , sublicense, and/or sell copies of the Software, and to permit persons
#    to whom the Software is furnished to do so,  subject to the above copy-
#    right notice and this permission notice shall being included in all 
#    copies or substantial portions of the Software.
#    NOTE: Full terms in `LICENSE` by setuptools distribution or git.

class Constants():
    """
    Define any local constants you wish to use. Add member variables or structs
    like namespace limits, bitmasks, commonly (ab)used constructs, or whatever.
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
