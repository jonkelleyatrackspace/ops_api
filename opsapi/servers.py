#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: servers.py
# ---
# © 2013, 2016, Jonathan Kelley <jon@uberleet.org> (github.com/jondkelley)
# ©             Anthony Tarola (github.com/atarola)
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

import logging
import sys

from tornado.httpserver import HTTPServer
from tornado.netutil import bind_unix_socket

log = logging.getLogger(__name__)


def https_server(application, options):
    """ https server """

    log.info("Binding application to unix socket {0}".format(
        options.unix_socket))
    if sys.version_info < (2, 7, 0):
        server = HTTPServer(application, ssl_options={
            "certfile": options.certfile,
            "keyfile": options.keyfile
        })
    else:
        server = HTTPServer(application, ssl_options={
            "certfile": options.certfile,
            "keyfile": options.keyfile,
            "ciphers": "HIGH,MEDIUM"
        })
    server.bind(options.port, options.address)
    server.start()


def http_server(application, options):
    """ http server """

    log.warn("Application is running in HTTP mode, this is insecure.  Pass in the --certfile and --keyfile to use SSL.")
    server = HTTPServer(application)
    server.bind(options.port, options.address)
    server.start()


def unix_socket_server(application, options):
    """ unix socket server """

    log.info("Binding application to unix socket {0}".format(
        options.unix_socket))
    server = HTTPServer(application)
    socket = bind_unix_socket(options.unix_socket)
    server.add_socket(socket)
