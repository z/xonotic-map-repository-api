from setuptools import setup
from setuptools import find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='xmra',
    version='0.3.0',
    description='Xonotic Map Repository Api',
    long_description=readme,
    author='Tyler Mulligan',
    author_email='z@xnz.me',
    url='https://github.com/z/xonotic-map-repository-api',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
       'console_scripts': [
          'xmra-add = xmra:main',
          'xmra-init = xmra.repositories.local.model:setup_db',
       ]
    },
    install_requires=required
)