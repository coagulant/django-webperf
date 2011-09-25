import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SITE_ID = 1
PROJECT_APPS = ('web_performance', 'test_app')
INSTALLED_APPS = ( 'django.contrib.auth',
                   'django.contrib.contenttypes',
                   'django.contrib.sessions',
                   'django.contrib.sites',
                   'django.contrib.admin',
                   'django_jenkins',) + PROJECT_APPS
DATABASE_ENGINE = 'sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        }
}
ROOT_URLCONF = 'tests.urls'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pylint',
)