from setuptools import setup, find_packages
f = open('./version')

major = 0
minor = int(f.readline())

version = f"{major}.{minor}"

setup(name='Python Java Stream',
      version=f'{version}',
      description='Java Stream implementation for Python',
      url='https://github.com/alemazzo/Python-Java-Stream',
      author='Alessandro Mazzoli',
      author_email='developer.alessandro.mazzoli@gmail.com',
      license='GNU',
      packages=find_packages(),
      keywords=['iterator', 'generator', 'stream', 'data',
                'functional', 'list', 'processing', 'java', 'filter', 'map', 'reduce', 'processing'],
      zip_safe=False)
