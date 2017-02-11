import os
from setuptools import find_packages
from setuptools import setup

from xmra import __author__, __email__, __url__, __license__, __version__, __summary__, __keywords__

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here, 'requirements.in')) as f:
    install_requires = f.read().splitlines()

try:
    import pypandoc
    readme_contents = pypandoc.convert(os.path.join(here, 'README.md'), 'rst')
    changelog_contents = pypandoc.convert(os.path.join(here, 'CHANGELOG.md'), 'rst')
except(IOError, ImportError):
    with open(os.path.join(here, 'README.md')) as f:
        readme_contents = f.read()
    with open(os.path.join(here, 'CHANGELOG.md')) as f:
        changelog_contents = f.read()

long_description = '{}\n{}'.format(readme_contents, changelog_contents)

setup(
    name='xmra',
    version=__version__,
    description=__summary__,
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.md', 'CHANGELOG.md', 'bin/*', 'config/*']},
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
       'console_scripts': [
          'xmra-add = bin.xmra:main',
          'xmra-init = bin.setup_db:main',
          'xmra-serve = bin.serve:main',
       ]
    },
    keywords=__keywords__,
)
