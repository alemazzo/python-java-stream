from os import path
from setuptools import setup, find_packages
f = open('./version')

major = 1
minor = int(f.readline())

version = f"{major}.{minor}"

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='java-stream',
      version=f'{version}',
      description='Java Stream implementation for Python',
      url='https://github.com/alemazzo/Python-Java-Stream',
      author='Alessandro Mazzoli',
      author_email='developer.alessandro.mazzoli@gmail.com',
      license='GNU',
      packages=['stream'],
      keywords=['query', 'iterator', 'generator', 'stream', 'data',
                'functional', 'list', 'processing', 'java', 'filter', 'map', 'reduce', 'processing'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )
