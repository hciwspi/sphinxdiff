#!/usr/bin/env python
"""Diff view for the sphinx documentation system"""

import os
from io import open
from setuptools import setup, find_packages
__version__ = '0.0.1'


this_dir = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(this_dir, 'readme.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sphinxdiff',
    version=__version__,
    url='https://github.com/hciwspi/sphinxdiff',
    license='MIT',
    author='Joachim Ballmann',
    author_email='jb@eberhardus.com',
    description=__doc__,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    py_modules = ['sphinxdiff'],
    packages=find_packages('src', exclude=['doc', 'templates',]),
    package_dir={'': 'src'},
    package_data={'sphinxdiff': ['htmltheme/static/css/sphinxdiff.css',
                                 'texinputs/sphinxdiff.sty']},
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Sphinx',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Utilities',
    ],
)

