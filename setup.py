#!/usr/bin/env python
# -*- coding: utf8 -*-

import setuptools


setuptools.setup(
    name="zeeguu",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Zeeguu Team",
    author_email="me@mir.lu",
    description="API for Zeeguu",
    keywords="second language acquisition api",
    dependency_links=('http://github.com/zacharyvoase/cssmin/'
                      'tarball/master#egg=cssmin-0.1.4',),
    install_requires=("flask>=0.10.1", "Flask-SQLAlchemy", "Flask-Assets",
                      "goose-extractor", "cssmin", "jsmin", "flask-wtf", "goslate", "MySQL-python")
)
