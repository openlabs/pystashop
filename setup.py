# -*- coding: utf-8 -*-
"""
    setup


    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup

execfile(os.path.join('pystashop', 'version.py'))

setup(
    name = 'pystashop',
    version=VERSION,
    url='https://github.com/openlabs/pystashop/',
    author='Sharoon Thomas, Openlabs Technologies',
    author_email='info@openlabs.co.in',
    description='Prestashop Webservice Python API Client',
    long_description=open('README.rst').read(),
    packages=['pystashop'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
        'lxml',
    ],
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests.suite',
)

