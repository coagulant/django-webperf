from django.core.management import execute_manager
import sys
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
                                     'tests',
                                     'django_jenkins'),
                   PROJECT_APPS = ('web_performance', 'tests'),
                   JENKINS_TASKS = (
                        'django_jenkins.tasks.with_coverage',
                        'django_jenkins.tasks.django_tests',
                        'django_jenkins.tasks.run_pep8',
                        'django_jenkins.tasks.run_pylint',
                   ))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv += ['test', 'tests']
    execute_manager(settings)
else:
    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner().run_tests(['tests',])
    if failures:
        sys.exit(failures)