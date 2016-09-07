#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: __init__.py
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

"""
This is the SDK for opsAPI. It is a submodule to the opsAPI package.

The opsAPI will utilize a few SDK calls to search&identify and build
a collection of extensions and their parameters (so it can do the API)

The rest of this is helper functions to make the abstract 'extension'
concept possible. Extension packs should be their own python modules, and
files in module are the 'extension'.
"""

from __future__ import absolute_import


# This SDK is subject to change. If you modify a public function, classname or method
# then look at what you should mark this change as below.
# - New Classes/Methods           = Minor Release
# - Rename/Delete Classes/Methods = Major Release
# The Tornado app will build a collection of extensions and check sdk compatability
# against the version below. If the version is not compatible then the extension
# will be excluded from the import into OPSAPI and a log message generated.
SDK_VERSION = "2.0"
# Extensions will be able to use > < macros in their definitions to take advantage
# of known specifics. Format is SDK_VERSION = "M.m" (M=major,m=minor)
