from setuptools import setup

version = '0.1.4.0'

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
    url='http://github.com/hoffmannkrzysztof/filmwebpy',
    license='GPL',
    packages=['filmweb','filmweb.parser'],
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
)
