#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: __init__.py
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

from __future__ import (print_function, absolute_import)

"""
OpsAPI is a lightweight API/HTTP framework in Tornado
which allows users to extend and prototype mid complexity
API designs and process solutions -- hours not weeks. I promise.

This is intended to empower systems engineers and developers
looking to cut the lifting out of running their ops shop.
Yes there's Rundeck/Jenkin's but you can't build a larger
platform on top of that -- this API is the missing loose
couple. Use the pluggable nature of this API and you can
hook Ansible, Fabric, or local Postgres bindings from Rundeck
OR Jenkins.

A real wizard could have multiple opsAPI deployments inter-
connected with Python-requests to create complex build pipelines
and processes. Then they would use the beautiful 
marmelab/ng-admin to create a browser app. Ditch 
Jenkins. Now where's the beach?
"""