import collections
import timeit
import unittest


_clock = timeit.default_timer


def _convertTimeUnit(value):
    if not value:
        return (value, '')

    prefixes = 'munpfa'
    level = 0
    while value < 1.0 and level < len(prefixes):
        value *= 1e3
        level += 1

    return (value, prefixes[level - 1] if level else '')


def _getBenchName(bench):
    return bench._testMethodName


class DummyResult(object):

    def wasSuccessful(self):
        return True


class BenchRunner(object):

    def run(self, bench):
        stack = collections.deque((bench,))
        while stack:
            obj = stack.popleft()
            if isinstance(obj, unittest.TestSuite):
                stack.extend(bench for bench in obj)
                continue

            function = getattr(obj, _getBenchName(obj))
            start = _clock()
            function()
            elapsed = _clock() - start
            elapsed, unit = _convertTimeUnit(elapsed)
            print("%s (%s.%s) ... %.3f %ss"
                  % (_getBenchName(obj), obj.__class__.__module__,
                     obj.__class__.__name__, elapsed, unit))

        return DummyResult()
