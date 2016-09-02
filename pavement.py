from paver.easy import *
import paver.doctools
from paver.setuputils import setup
import shutil, os

setup(
    name="opsapi",
    version="0.3",
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description="Extensible operations API and SDK blueprint examples",
    url="https://github.com/jonkelleyatrackspace/ops_api",
    packages=['opsapi'],
    install_requires=['pyyaml==3.10','tornado==3.0.1','toro==0.5','passlib==1.6' ],
    entry_points={
        'console_scripts': [
            'opsapi = opsapi.server:main'
        ]
    },
    zip_safe=False
)

def chmod_dash_r(path, mode):
    """
    Recursively runs chmod under a path with mode.
    """
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)

@task
@needs('install')
def load_blueprints(options):
    """
    Sets up the ops blueprints
    """
    if os.path.isdir("/srv/blueprints"):
        shutil.rmtree("/srv/blueprints")
    shutil.copytree("./srv/blueprints",("/srv/blueprints"))
    chmod_dash_r("/srv/blueprints", 0755)

@task
@needs('load_blueprints')
def start():
    """
    Start a dev instance for test
    """
    sh('opsapi --dir=/srv/blueprints')

@task
def clean(options):
    """
    Cleanup after paver operations
    """
    for i in ['./dist', './build', './opsapi.egg-info']:
        print("Removing {file}".format(file=i))
        try:
            shutil.rmtree(i)
        except OSError:
            pass
