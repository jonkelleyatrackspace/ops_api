#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: util.py
# authors: jonathan kelley, anthony tarola
# ---
# license: the mit license
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the above copyright notice and this permission notice shall being included
# in all copies or substantial portions of the Software.

import os
import pkgutil
import logging
import sys

import tornado.web

from opsapi.config import config
from opsapi.extensions import create_collection

log = logging.getLogger(__name__)


class route(object):
    """
    decorates RequestHandlers and builds up a list of routables handlers

    From: https://gist.github.com/616347
    """

    _routes = []

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    def __call__(self, _handler):
        """gets called when we class decorate"""

        log.info("Binding {0} to route {1}".format(
            _handler.__name__, self._uri))
        name = self.name and self.name or _handler.__name__
        self._routes.append(tornado.web.url(self._uri, _handler, name=name))
        return _handler

    @classmethod
    def get_routes(self):
        return self._routes


def setup_logging():
    """ setup the logging system """

    base_log = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"))
    base_log.addHandler(handler)
    base_log.setLevel(logging.DEBUG)
    return handler


def create_application(debug):
    # import the handler file, this will fill out the route.get_routes() call.
    import opsapi.handlers

    application = tornado.web.Application(
        route.get_routes(),
        extensions=create_collection(config['directory']),
        debug=debug
    )

    return application
