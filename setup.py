"""
"""
from setuptools import setup

import trackopy


with open('README.md') as r:
    readme = r.read()


setup(
    name=trackopy.__title__,
    version=trackopy.__version__,
    url='https://github.com/ThaWeatherman/trackopy',
    license='MIT',
    author='Sean Beck',
    author_email='seanmckaybeck@gmail.com',
    description='Python wrapper for the Trackobot API',
    long_description=readme,
    packages=['trackopy'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3'
    ],
    test_suite='tests',
    keywords='trackobot hearthstone'
)

