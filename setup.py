from setuptools import setup

version = '0.1.1.2'

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
    packages=['filmweb','filmweb.parser'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
)