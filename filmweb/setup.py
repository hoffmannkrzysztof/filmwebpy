from setuptools import setup, find_packages
import os

from distutils.core import Extension

version = '0.1'


setup(name='filmwebpy',
    version=version,
    description="Python parser for Filmweb",
    long_description=open("README").read(),
    classifiers=[
        "Programming Language :: Python",
        ],
    keywords='python filmweb parser',
    author='Krzysztof Hoffmann',
    author_email='krzysiekpl@gmail.com',
    url='http://github.com/krzysiekpl/filmwebpy',
    license='GPL',
    packages=find_packages(),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
)