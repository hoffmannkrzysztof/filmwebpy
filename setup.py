from setuptools import setup

version = '0.1.5.1'

setup(name='filmwebpy',
      version=version,
      description="Python parser for Filmweb",
      long_description=open("README").read(),
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='python filmweb parser',
      author='Krzysztof Hoffmann',
      author_email='krzysztof.hoffmann@increase.pl',
      url='http://github.com/hoffmannkrzysztof/filmwebpy',
      license='GPL',
      packages=['filmweb', 'filmweb.parser'],
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools', 'beautifulsoup4'
      ],
)
