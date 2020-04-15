"""
Create ask_jc as a Python package
"""

from __future__ import print_function
import io
import os
import os.path
import sys

from setuptools import setup, find_packages


MIN_PYTHON_VERSION = (3, 6)

PKGNAME = 'ask_jc'
DESC = '''
An notebooks of information extraction from Covid19 research papers
'''

# --------------------------------------------------------------------

def pkg_version():
    """Read the package version from VERSION.txt"""
    basedir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(basedir, 'VERSION.txt'), 'r') as f:
        return f.readline().strip()

def parse_requirements(filename='requirements.txt'):
    """Read the requirements file"""
    pathname = os.path.join(os.path.dirname(__file__), filename)
    modules = []
    urls = []
    with io.open(pathname, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                urls.append(line)
            else:
                modules.append(line)
    return modules, urls

# --------------------------------------------------------------------

VERSION = pkg_version()

if sys.version_info < MIN_PYTHON_VERSION:
    sys.exit('**** Sorry, {} {} needs at least Python {}'.format(
        PKGNAME, VERSION, '.'.join(map(str, MIN_PYTHON_VERSION))))

install_requires, dependency_links = parse_requirements()

setup_args = dict(
    # Metadata
    name=PKGNAME,
    version=VERSION,
    description=DESC.split('\n')[0],
    long_description=DESC,
    license='(c) Accenture',
    author='Javier Sastre',
    author_email='j.sastre.martinez@accenture.com',

    # Locate packages
    packages=find_packages('src'),  # [ PKGNAME ],
    package_dir={'': 'src'},

    # Requirements
    python_requires='>='+'.'.join(map(str, MIN_PYTHON_VERSION)),
    install_requires=install_requires,
    dependency_links=dependency_links,
    # Optional requirements
    extras_require={
        'test': ['pytest', 'nose', 'coverage'],
    },

    entry_points={'console_scripts': [
        'ask_jc_extract_paper_sentences = ask_jc.extract_paper_sentences:main',
        'ask_jc_index_sentences = ask_jc.index_sentences:main',
        'ask_jc_sentences_to_dataframe = ask_jc.sentences_to_dataframe:main'
    ]},

    # pytest requirements
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    # More metadata
    keywords=['Accenture', 'The Dock', 'COVID-19', 'COVID', 'coronavirus', 'nlp'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)


if __name__ == '__main__':
    setup(**setup_args)
