#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi: set ft=python :
# file: config.py
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

import copy
import logging
import yaml

log = logging.getLogger(__name__)

# Contains default mappings before yaml loads
default_mappings = {}
default_mappings['disable_debug_console'] = False
default_mappings['output_highlighter'] = False


class Config(dict):
    """ Configuration dictionary """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def load_file(self, file_name):
        log.info("loading config singleton from file {n}".format(n=file_name))
        data = yaml.load(open(file_name, 'r'))

        if not isinstance(data, dict):
            raise Exception("config file not parsed correctly")

        log.info("objects in config {objs}".format(objs=data))
        deep_merge(self, data)


def deep_merge(orig, other):
    """ Modify orig, overlaying information from other """

    for key, value in other.items():
        if key in orig and isinstance(orig[key], dict) and isinstance(value, dict):
            deep_merge(orig[key], value)
        else:
            orig[key] = value

#
# Singleton Instance
#

config = Config()
