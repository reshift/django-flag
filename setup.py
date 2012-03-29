# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
  name='django-hub-flag',
  version='0.2.2',
  description='Flags for django',
  long_description=long_description,
  author='Sjoerd Arendsen',
  author_email='s.arendsen@hub.nl',
  url='https://github.com/hub-nl/nl.hub.django.app.flag/',
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