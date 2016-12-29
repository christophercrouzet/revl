import codecs
import os
import re
import setuptools


def findVersion(*filePaths):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *filePaths), 'r', 'utf8') as f:
        versionFile = f.read()

    versionMatch = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                             versionFile, re.M)
    if versionMatch:
        return versionMatch.group(1)

    raise RuntimeError("Unable to find the version string.")


setuptools.setup(
    name='revl',
    version=findVersion('revl.py'),
    description="Helps to benchmark code for Autodesk Maya",
    keywords='Autodesk Maya API benchmark test',
    license='MIT',
    url='https://github.com/christophercrouzet/revl',
    author='Christopher Crouzet',
    author_email='christopher.crouzet@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    packages=[],
    py_modules=['revl'],
    include_package_data=True
)
