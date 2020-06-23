from setuptools import setup, find_packages
import os
import sys

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in reqs]

setup(name='rest-app',
      version='1.0.1',
      description='Rest Application for DB access',
      license='Apache 2.0',
      author='Basabjit',
      author_email='basab401@yahoo.co.in',
      python_requires='>=3.6.*',
      packages=find_packages(),
      install_requires=requirements,
      classifiers=[
        'Intended Audience :: Linux Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
      ],
      keywords=['flask']
)

