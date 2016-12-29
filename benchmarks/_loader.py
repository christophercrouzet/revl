import unittest


class BenchLoader(unittest.TestLoader):
    testMethodPrefix = 'bench'
