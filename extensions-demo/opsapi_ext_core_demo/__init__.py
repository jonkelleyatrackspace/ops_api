#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vi: set ft=python :
# file: __init__.py

from __future__ import absolute_import
from opsapi.sdk import __version__ as SDK_VERSION
from opsapi.sdk import PotentialSdkIncompatabilityWarning
from distutils.version import LooseVersion, StrictVersion
import warnings

import test
# How to expose this function
# import opsapi_ext_core_demo
# print(opsapi_ext_core_demo.test.parameter.collection)
# {'age': <opsapi_ext_core_demo.test.age instance at 0x7f87011bd7a0>, 'name': <opsapi_ext_core_demo.test.name instance at 0x7f87011a80e0>}


"""
This is a demo extension pack for opsAPI.
Using the v2.0 SDK.

This python module, or 'extension pack', contains
a set python files or 'extensions', that get loaded
as API request extensions in opsAPI. You can perform
jobs or operations in each file.

"""

# The version of this extension
__VERSION__ = StrictVersion("1.0")

if SDK_VERSION > __VERSION__:
  print("HEY: The SDK version is newer then this extension supports.")
  warnings.warn('The SDK version is newer then this extension supports.',
    PotentialSdkIncompatabilityWarning)