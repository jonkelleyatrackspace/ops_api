#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: constants.py
# desc: constant literals for reference
# ---
# © 2016, Jonathan Kelley <jon@uberleet.org> (github.com/jondkelley)
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

from __future__ import (print_function, absolute_import)

"""
This file defines constant structures for which you can reference or inherit from.
Think HTTP codes, max open file descriptors, thats what I'd put in here.

This can be leveraged in the SDK, and by extension in the constants namespace
in any extension modules.
"""


class BaseConstants:
    """
    Define any local constants you wish to use. Add member variables or structs
    like namespace limits, bitmasks, commonly (ab)used constructs, or whatever.
    """

