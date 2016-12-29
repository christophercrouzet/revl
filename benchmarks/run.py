#!/usr/bin/env mayapy

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import collections
import optparse
import sys
import unittest

from benchmarks._loader import BenchLoader
from benchmarks._runner import BenchRunner


def _findBenchs(path, selectors=None):
    if selectors is None:
        def filter(bench):
            return True
    else:
        def filter(bench):
            return any(selector in _getBenchFullName(bench)
                       for selector in selectors)

    out = []
    stack = collections.deque(
        (BenchLoader().discover(path, pattern='bench*.py'),))
    while stack:
        obj = stack.popleft()
        if isinstance(obj, unittest.TestSuite):
            stack.extend(bench for bench in obj)
        elif type(obj).__name__ == 'ModuleImportFailure':
            try:
                # This should always throw an ImportError exception.
                getattr(obj, _getBenchName(obj))()
            except ImportError as e:
                sys.exit(e.message.strip())
        elif filter(obj):
            out.append(obj)

    return out


def _getBenchName(bench):
    return bench._testMethodName


def _getBenchFullName(bench):
    return '%s.%s.%s' % (bench.__class__.__module__, bench.__class__.__name__,
                         _getBenchName(bench))


def main():
    usage = "usage: %prog [bench1..benchN]"
    parser = optparse.OptionParser(usage=usage)

    _, args = parser.parse_args()

    selectors = args if args else None
    benchs = _findBenchs(_HERE, selectors)

    suite = BenchLoader().suiteClass(benchs)
    BenchRunner().run(suite)


if __name__ == "__main__":
    main()
