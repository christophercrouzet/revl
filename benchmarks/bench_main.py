#!/usr/bin/env mayapy

import maya.standalone
maya.standalone.initialize()

import os
import sys
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_HERE, os.pardir)))


import unittest

from maya import OpenMaya

import revl

from benchmarks._loader import BenchLoader
from benchmarks._runner import BenchRunner


class MainBench(unittest.TestCase):

    def benchCreatePrimitive1(self):
        count = 5000
        commands = [
            (1.0, revl.createPrimitive,)
        ]
        revl.run(commands, count)

    def benchCreatePrimitive2(self):
        count = 5000
        commands = [
            (1.0, revl.createPrimitive, (), {'type': revl.PrimitiveType.POLY_CUBE})
        ]
        revl.run(commands, count)

    def benchCreatePrimitive3(self):
        count = 5000
        commands = [
            (1.0, revl.createPrimitive, (), {'name': 'primitive'})
        ]
        revl.run(commands, count)

    def benchCreatePrimitive4(self):
        count = 5000
        commands = [
            (1.0, revl.createPrimitive, (), {'parent': True})
        ]
        revl.run(commands, count)

    def benchCreateTransform1(self):
        count = 5000
        commands = [
            (1.0, revl.createTransform,)
        ]
        revl.run(commands, count)

    def benchCreateTransform2(self):
        count = 5000
        commands = [
            (1.0, revl.createTransform, (), {'name': 'xform'})
        ]
        revl.run(commands, count)

    def benchCreateTransform3(self):
        count = 5000
        commands = [
            (1.0, revl.createTransform, (), {'parent': True})
        ]
        revl.run(commands, count)


if __name__ == '__main__':
    unittest.main(testLoader=BenchLoader(), testRunner=BenchRunner)
