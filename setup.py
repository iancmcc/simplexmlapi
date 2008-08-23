#!/usr/bin/env python

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

version = '0.1.1'
LONG_DESCRIPTION = """
simplexmlapi provides an easy way to access XML data. It is pure Python code with no dependencies.

simplexmlapi uses the xml.dom.minidom module to parse XML data, then allows the resulting document to be walked using a dotted name syntax. It also provides a SimpleXmlApi object which comprises mappings of attributes to dotted-name paths.

The SimpleXmlApi object may be subclassed to provide simple APIs for known data structures.
"""

setup(name='simplexmlapi',
      version=version,
      description="Simple, fast way to create read-only APIs for XML data",
      long_description=LONG_DESCRIPTION,
      classifiers=[
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python'
      ], 
      author='Ian McCracken',
      author_email='ian.mccracken@gmail.com',
      url='http://code.google.com/p/simplexmlapi/',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      platforms=['any'],
      zip_safe=True
      )
