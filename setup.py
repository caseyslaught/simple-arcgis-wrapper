import os
import sys

from setuptools import setup

version = '1.0.1'

long_description = open('README.md').read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='simple-arcgis-wrapper',
    version=version,
    author='Casey Slaught',
    author_email='casey@caracal.cloud',
    description='A simple wrapper for interacting with the ArcGIS Online REST API.',
    keywords='arcgis gis rest api wrapper',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/caracal-cloud/simple-arcgis-wrapper',

    packages=['simple_arcgis_wrapper'],
    python_requires=">=3.5",
    install_requires=[
        'requests>=2.10.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)