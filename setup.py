#!/usr/bin/env python

# Remove .egg-info directory if it exists, to avoid dependency problems with
# partially-installed packages (20160119/dphiffer)

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/mapzen.whosonfirst.meta.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read()
version = open("VERSION").read()

setup(
    name='mapzen.whosonfirst.meta',
    namespace_packages=['mapzen', 'mapzen.whosonfirst'],
    version=version,
    description='Simple Python utilities for working with Who\'s On First meta files',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-meta',
    packages=packages,
    scripts=[
        'scripts/wof-default-meta',
        'scripts/wof-dump-meta',
        'scripts/wof-update-meta',
        ],
    download_url='https://github.com/whosonfirst/py-mapzen-whosonfirst-meta/releases/tag/' + version,
    license='BSD')
