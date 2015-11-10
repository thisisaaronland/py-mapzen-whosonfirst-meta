#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.meta',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.meta'],
    version='0.1',
    description='Simple Python utilities for working with Who\'s On First meta files',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-meta',
    install_requires=[
        'geojson',
        ],
    dependency_links=[
        ],
    packages=packages,
    scripts=[
        'scripts/wof-dump-meta',
        ],
    download_url='https://github.com/mapzen/py-mapzen-whosonfirst-meta/releases/tag/v0.1',
    license='BSD')
