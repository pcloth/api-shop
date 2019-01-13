#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='api-shop',
    version=0.12,
    description=(
        'RESTful api shop for django or flask'
    ),
    long_description=open('README.rst', encoding='utf-8').read(),
    author='pcloth',
    author_email='pcloth@gmail.com',
    maintainer='pcloth',
    maintainer_email='pcloth@gmail.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,    # 启用清单文件MANIFEST.in
    exclude_package_date={'':['.gitignore']},
    platforms=["all"],
    url='https://github.com/pcloth/api-shop',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
