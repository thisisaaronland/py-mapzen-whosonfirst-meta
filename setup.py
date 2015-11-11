#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='mapzen.whosonfirst.meta',
    namespace_packages=['mapzen', 'mapzen.whosonfirst', 'mapzen.whosonfirst.meta'],
    version='0.4',
    description='Simple Python utilities for working with Who\'s On First meta files',
    author='Mapzen',
    url='https://github.com/mapzen/py-mapzen-whosonfirst-meta',
    install_requires=[
        'geojson',
        'atomicwrites',
        'mapzen.whosonfirst.utils>=0.12',
        ],
    dependency_links=[
        'https://github.com/whosonfirst/py-mapzen-whosonfirst-utils/tarball/master#egg=mapzen.whosonfirst.utils-0.12',
        ],
    packages=packages,
    scripts=[
        'scripts/wof-dump-meta',
        ],
    download_url='https://github.com/mapzen/py-mapzen-whosonfirst-meta/releases/tag/v0.4',
    license='BSD')
