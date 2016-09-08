#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: pavement.py
# desc: Setuputils and Paver configure/install components
# authors: jonathan kelley 2016

from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import shutil
import os
import platform
from paver.easy import pushd



"""
Setuputils / Paver setup
Paver performs our setuputils tasks, in addition to configure
tasks without utilizing the full extent of Makefile.
This basically feeds off Makefile and calls the appropriate
setup function. Handy eh?

Just be sure to keep your Paver <> Makefile alias/pointer
references up to date! :)

TODO: NOTE:
`make` in Makefile should call paver task to install
extensions, and then opsAPI. Extensions are headless.
TODO: NOTE:
make extension(name) should build a particular extension
(make this distributable in cwd as extension too for git)
"""

def value_from_specfile(getkey):
    """
    loads the version and other keys from the .spec file
    which shall be our source of truth for versioning.

    i looked into using rpm, but the library is really really unwieldy
    not an external api, and looks like it's likely to change
    """
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".spec"):
            SPEC_FILE = file

    spec = {}
    with open(SPEC_FILE, "r") as f:
        for line in f.readlines():
            try:
                value = line.split(":")[1].lstrip().strip()
                key = line.split(":")[0].lstrip().lower().rstrip()

                spec[key] = value
            except:
                pass
        return spec[getkey]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

install_requires = [
    'pyyaml==3.10',
    'tornado==3.0.1',
    'toro==0.5',
    'passlib==1.6'
]
install_requires = []
setup(
    name=value_from_specfile('name'),
    version=value_from_specfile('version'),
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description=value_from_specfile('summary'),
    url=value_from_specfile('url'),
    packages=[str(value_from_specfile('name'))],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
             '{name} = {name}.server:main'.format(
                 name=value_from_specfile('name'))
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: System :: Operating System",
    ],
    zip_safe=False
)

@needs('install_extensions')
@needs('install')
def install_all():
    """
    This is just a dummy task that
    installs opsapi+exensions with a
    require decorator.
    """
    pass

@task
@cmdopts([
    ('extension=', 'e', 'Directory of extension to install')
])
def install_extension():
    """
    When given the -e parameter it will install an extension
    in a subdirectory with `paver install`
    """
    if not hasattr(options, "extension"):
        print("{0}Missing options, use -e or --help{1}".format(
            bcolors.FAIL,
            bcolors.ENDC))
        exit(1)
    else:
        arg = options.extension
        print("{x}Run install task for "
        " {extension}{y}".format(
            extension=arg,
            x=bcolors.OKGREEN,
            y=bcolors.ENDC))
    with pushd(arg):
        sh("paver install".format(
            dir=arg))

@task
@might_call('install_extension')
def install_extensions():
    """
    This will iterate through your CWD and go into
    any dir matching extensions-*. If a pavement.py
    is inside this directory, run paver install.
    """
    cwd = str(os.getcwd())
    cwd_dirs = [ name for name in
     os.listdir(cwd) if 
     os.path.isdir(os.path.join(cwd, name))
     ] # comprehend a list of dirnames in cwd
    will_install = []
    for directory in cwd_dirs:
        paver = "{x}/pavement.py".format(x=directory)
        if directory.startswith('extensions-') and os.path.isfile(paver):
            call_task('install_extension',
                options={
                    'extension' : directory
                })

@task
def clean(options):
    """
    CLEAN after paver build operations
    """
    for i in ['./dist', './build', './opsapi.egg-info']:
        print("Removing {file}".format(file=i))
        try:
            shutil.rmtree(i)
        except OSError:
            pass
