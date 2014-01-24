#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name='django-model-gettext',
      version=0.01,
      url='https://github.com/scaryclam/django-model-gettext',
      author="Becky Lewis",
      author_email="github@scaryclam.co.uk",
      description="Translation mixin for writing models into .po files",
      long_description=open('README.rst').read(),
      keywords="Rosetta, Django, gettext, models, translation",
      license='MIT',
      platforms=['linux'],
      packages=find_packages(exclude=['tests*']),
      include_package_data=True,
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: MIT',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Topic :: Other/Nonlisted Topic'],
      install_requires=[
          'django>=1.4',
      ],
      )

