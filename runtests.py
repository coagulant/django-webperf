import os, sys
from django.conf import settings

settings.configure(DEBUG = True,
                   DATABASE_ENGINE = 'sqlite3',
                   DATABASES = {
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                            }
                   },
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'web_performance',
                                     'tests',))

from django.test.simple import DjangoTestSuiteRunner
failures = DjangoTestSuiteRunner().run_tests(['tests',])
if failures:
    sys.exit(failures)