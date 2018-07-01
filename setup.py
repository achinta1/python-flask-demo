from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(version='1.0',
      name='login',
      description='Simple Flask-based login service',
      packages=['app'],
      install_requires=[
          # Flask is kinda crucial :)
          'Flask==1.0.2',

          # Other libs we explicitly used
          'Flask-SQLAlchemy',
          'Flask-WTF',
          'SQLAlchemy',
          'Flask-Migrate',
          'Flask-Script',
          'Flask-Testing',
          'Flask-Bcrypt',
          'Flask-Login',
          'Flask-RESTful',
          'pytest',

          # Automatic deps as brought in when I pip installed Flask
          'Jinja2',
          'MarkupSafe',
          'Werkzeug',
          'argparse',
          'itsdangerous',
          'wsgiref',
          'py',
          # new added  those are optional deps
          'click',
          'blinker',
          'simplejson',
          # Python API library and shell utilities to monitor file system events. Watchdog provides a faster, more efficient reloader for the development server
          'watchdog',

          # Other automatic deps
          'Tempita',
          'WTForms',
          'decorator',
          'pbr',
          'six',
          'Mako',
          'alembic',
          'py-bcrypt',
          'aniso8601',
          'pytz',
      ],
      tests_require=['pytest'],
      cmdclass = {'test': PyTest},
)
