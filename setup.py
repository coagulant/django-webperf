try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

tests_require = [
    'Django>=1.2,<1.4',
    'mock==0.7.2',
    'django-jenkins>=0.11.1'
]

setup(
    name='django-webperf',
    version='0.1dev',
    author='Ilya Baryshev',
    author_email='baryshev@gmail.com',
    packages=find_packages(exclude=("tests")),
    url='https://github.com/futurecolors/django-webperf',
    license='MIT',
    description="A collection of stuff to improve django web performance.",
    long_description=open('README.rst').read(),
    install_requires=[
        "django-appconf==0.4.1"
    ],
    tests_require=tests_require,
    test_suite = "runtests",
    extras_require={'test': tests_require},
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)