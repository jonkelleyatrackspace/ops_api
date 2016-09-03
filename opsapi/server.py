#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: server.py
# authors: anthony tarola
# ---
# license: the mit license
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the above copyright notice and this permission notice shall being included
# in all copies or substantial portions of the Software.

import logging

from tornado.ioloop import IOLoop

from opsapi.options import command_line_options
from opsapi.util import setup_logging, create_application
from opsapi.servers import http_server, https_server, unix_socket_server

log = logging.getLogger(__name__)


def main():
    """ entry point for the application """

    # get the command line options
    options = command_line_options()
    setup_logging()

    # setup the application
    log.info("Setting up the application")
    application = create_application(options.debug)

    # warn about --force-json
    if options.force_json:
        log.warn("Application started with '--force-json' option.  All calls will be treated as if they passed the 'Content-Type: application/json' header.  This may cause unexpected behavior.")

    # server startup
    if options.unix_socket:
        unix_socket_server(application, options)
    elif options.certfile and options.keyfile:
        https_server(application, options)
    else:
        http_server(application, options)

    # start the ioloop
    log.info("xxxxxxxxxxthe IOLoddsopxx")
    IOLoop.instance().start()
