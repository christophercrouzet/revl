#!/usr/bin/env mayapy

import collections
import optparse
import os
import subprocess
import sys
import unittest


def _findTests(path, selectors=None):
    if selectors is None:
        def filter(test):
            return True
    else:
        def filter(test):
            return any(selector in _getTestFullName(test)
                       for selector in selectors)

    out = []
    stack = collections.deque((unittest.TestLoader().discover(path),))
    while stack:
        obj = stack.popleft()
        if isinstance(obj, unittest.TestSuite):
            stack.extend(test for test in obj)
        elif type(obj).__name__ == 'ModuleImportFailure':
            try:
                # This should always throw an ImportError exception.
                getattr(obj, _getTestName(obj))()
            except ImportError as e:
                sys.exit(e.message.strip())
        elif filter(obj):
            out.append(obj)

    return out


def _getTestName(test):
    return test._testMethodName


def _getTestFullName(test):
    return '%s.%s.%s' % (test.__class__.__module__, test.__class__.__name__,
                         _getTestName(test))


def main():
    usage = "usage: %prog [options] [test1..testN]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        '-s', '--split', action='store_true', dest='split',
        help="run each test in a separate subprocess"
    )

    (options, args) = parser.parse_args()

    here = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.abspath(os.path.join(here, os.pardir))
    sys.path.insert(0, rootPath)

    selectors = args if args else None
    tests = _findTests(here, selectors)

    if options.split:
        for test in tests:
            name = _getTestFullName(test)
            subprocess.call([sys.executable, '-m', 'unittest', '-v', name],
                            env={'PYTHONPATH': ':'.join(sys.path)})
    else:
        suite = unittest.TestLoader().suiteClass(tests)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
