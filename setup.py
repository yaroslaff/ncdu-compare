from setuptools import setup
import os
import sys
from importlib.machinery import SourceFileLoader


def get_version(path):
    foo = SourceFileLoader(os.path.basename(path),"ncdu-compare").load_module()
    return foo.version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = get_version('./ncdu_compare')

setup(name='ncdu-compare',
      version=version,
      description='ncdu-compare',
      url='https://github.com/yaroslaff/ncdu-compare',
      author='Yaroslav Polyakov',
      author_email='yaroslaff@gmail.com',
      license='MIT',
      packages=[],
      scripts=['ncdu-compare'],
      # include_package_data=True,

      long_description = read('README.md'),
      long_description_content_type='text/markdown',

      install_requires=[],
      zip_safe=False
      )

