#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='pandas_schema',
    version='0.3.2',
    description='A validation library for Pandas data frames using user-friendly schemas',
    url='https://github.com/TMiguelT/PandasSchema',
    author='Michael Milton',
    author_email='michael.r.milton@gmail.com',
    license='MIT',
    test_suite='test',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='pandas csv verification schema',
    packages=find_packages(),
    install_requires=['matplotlib', 'dnaplotlib'],
)
