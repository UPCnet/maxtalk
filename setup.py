import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_who',
    'pymongo',
    'gevent-socketio',
    'pyramid_socketio'

    ]

test_requires = ['WebTest', 'mock', ]

setup(name='maxtalk',
      version='3.0',
      description='MAX realtime talk service',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='UPCnet Content Management Team',
      author_email='victor.fernandez@upcnet.es',
      url='http://github.com/upcnet/maxtalk',
      keywords='web pylons pyramid mongodb',
      packages=['maxtalk'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires + test_requires,
      test_suite="maxtalk.tests",
      extras_require={
        'test': ['WebTest', 'mock', ]
      },
      entry_points="""\
      [paste.app_factory]
      main = maxtalk:main
      """,
      )
