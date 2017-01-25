import io
import os
import re
import setuptools


def _read(*paths, **kwargs):
    # Credits: https://packaging.python.org/single_source_version.
    here = os.path.dirname(__file__)
    encoding = kwargs.get('encoding', 'utf8')
    with io.open(os.path.join(here, *paths), encoding=encoding) as f:
        return f.read()


def _getMetas(*filePaths):
    data = _read(*filePaths)
    out = {}
    metas = ('author', 'contact', 'license', 'summary', 'title', 'url',
             'version')
    for meta in metas:
        pattern = r'^__%s__ = u?[\'"]([^\'"]*)[\'"]' % (meta,)
        match = re.search(pattern, data, re.MULTILINE)
        if match is None:
            raise RuntimeError("Unable to find the metadata '%s'." % (meta,))

        out[meta] = match.group(1)

    return out


_METAS = _getMetas('revl.py')

setuptools.setup(
    name=_METAS['title'],
    version=_METAS['version'],
    description=_METAS['summary'],
    url=_METAS['url'],
    author=_METAS['author'],
    author_email=_METAS['contact'],
    license=_METAS['license'],
    keywords='Autodesk Maya API benchmark benchmarking test',
    long_description=_read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    extras_require={
        'dev': ['coverage', 'pycodestyle', 'pydocstyle', 'pylint',
                'sphinx>=1.3'],
        'docs': ['sphinx>=1.3'],
    },
    packages=[],
    py_modules=['revl'],
    include_package_data=True
)
