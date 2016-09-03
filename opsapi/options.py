#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: options.py
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

from optparse import OptionParser, IndentedHelpFormatter

from opsapi.config import config


def command_line_options():
    """ command line configuration """

    parser = OptionParser(usage="usage: %prog [options] <htpasswd>")

    parser.formatter = PlainHelpFormatter()
    parser.description = """This will expose a set of opsapi extensions as a REST API.

Note: Please make sure this application is behind authentication for security.
Please use the SSL config options, give a passwd file, and either whitelist
access to the API via firewall or keep it on a privately routed network.

Use the apache htpasswd utility to create your htpasswd files."""

    parser.add_option('-d', '--debug', action="store_true", dest="debug", default=False,
                      help="Start the application with debug enabled.")

    parser.add_option('--dir', action="store", dest="directory", default="/srv/extensions",
                      help="Directory to load SDK extensions from")

    parser.add_option('--force-json', action="store_true", dest="force_json", default=False,
                      help="Force the application to treat all incoming requests as 'Content-Type: application/json'")

    parser.add_option('-p', '--port', action="store", dest="port", default=3000,
                      help="The listening port")

    parser.add_option('-a', '--address', action="store", dest="address", default=None,
                      help="Listening interface. Can be a hostname or an IPv4/v6 address.")

    parser.add_option('-c', '--certfile', action="store", dest="certfile", default=None,
                      help="SSL Cert File")

    parser.add_option('-k', '--keyfile', action="store", dest="keyfile", default=None,
                      help="SSL Private Key File")

    parser.add_option('-u', '--unix-socket', action="store", dest="unix_socket", default=None,
                      help="Bind opsapi to a unix domain socket")

    options, args = parser.parse_args()

    # TODO: only do this if they specify the ssl certfile and keyfile
    if len(args) >= 1:
        config['passfile'] = args[0]
    else:
        config['passfile'] = None

    config['directory'] = options.directory
    config['force_json'] = options.force_json

    return options


class PlainHelpFormatter(IndentedHelpFormatter):

    def format_description(self, description):
        if description:
            return description + "\n"
        else:
            return ""
