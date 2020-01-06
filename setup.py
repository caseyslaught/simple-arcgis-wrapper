import os
import sys

from setuptools import setup

version = '0.1'

long_description = open('README.md').read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='simple-arcgis-wrapper',
    version=version,
    packages=['simple_arcgis_wrapper'],
    description='A simple wrapper for interacting with the ArcGIS Online REST API.',
    data_files=[('', ['README.md'])],
    license='MIT',
    author='Caracal',
    install_requires=[
        'requests>=v2.22.0'
    ],
    python_requires=">=2.7.10",
    author_email='casey@caracal.cloud',
    url='https://github.com/caracal-cloud/simple-arcgis-wrapper',
    keywords='arcgis rest api',
    classifiers=[],
    long_description=long_description,
    long_description_content_type='text/markdown'
)