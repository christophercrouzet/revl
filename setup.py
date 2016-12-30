import io
import os
import re
import setuptools


def read(*names, **kwargs):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.dirname(__file__)
    encoding = kwargs.get('encoding', 'utf8')
    with io.open(os.path.join(here, *names), encoding=encoding) as fp:
        return fp.read()


def findVersion(*filePaths):
    # Credits: https://packaging.python.org/single_source_version.
    versionFile = read(*filePaths)
    versionMatch = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                             versionFile, re.M)
    if versionMatch:
        return versionMatch.group(1)

    raise RuntimeError("Unable to find the version string.")


setuptools.setup(
    name='revl',
    version=findVersion('revl.py'),
    description="Helps to benchmark code for Autodesk Maya",
    long_description=read('README.rst'),
    keywords='Autodesk Maya API benchmark test',
    license='MIT',
    url='https://github.com/christophercrouzet/revl',
    author="Christopher Crouzet",
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
