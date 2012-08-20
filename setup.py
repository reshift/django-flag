# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
  name='django-flag',
  version='2.0.5',
  description='Flags for django',
  long_description=long_description,
  author='Sjoerd Arendsen',
  author_email='s.arendsen@hub.nl',
  url='https://github.com/hub-nl/django-flag/',
  packages=(
    'flag',
    'flag.templatetags',
  ),
  package_data={
    'flag': [
      'templates/flag/*',
    ]
  },
  zip_safe=False,
)