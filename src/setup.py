#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
import re, ast, pathlib



_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('api_shop/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


setup(
    name='api-shop',
    version=version,
    description=(
        'RESTful api shop for django or flask or bottle'
    ),
    long_description=pathlib.Path('README.MD').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    author='pcloth',
    author_email='pcloth@gmail.com',
    maintainer='pcloth',
    maintainer_email='pcloth@gmail.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True, 
    exclude_package_date={'':['.gitignore']},
    keywords=['api-shop', 'Flask-RESTful', 'Django REST framework', 'RESTful'],
    platforms=["all"],
    url='https://github.com/pcloth/api-shop',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)
