from os import path
import codecs
from setuptools import setup, find_packages

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

tests_require = [
    'Django>=1.2,<1.4',
    'mock==0.7.2',
]

setup(
    name='django-webperf',
    version='0.1',
    author='Ilya Baryshev',
    author_email='baryshev@gmail.com',
    packages=find_packages(exclude=("tests")),
    url='https://github.com/coagulant/django-webperf',
    license='MIT',
    description="A collection of stuff to improve django web performance.",
    long_description=read(path.join(path.dirname(__file__), 'README.rst')),
    install_requires=[
        "django-appconf==0.4.1"
    ],
    tests_require=tests_require,
    test_suite = "runtests",
    extras_require={'test': tests_require},
    classifiers = [
        'Development Status :: 7 - Inactive',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
