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


globalA = 0
globalB = 0


def incrementA(context):
    global globalA
    globalA += 1


def incrementB(context):
    global globalB
    globalB += 1


class MainTest(unittest.TestCase):

    def setUp(self):
        global globalA, globalB
        OpenMaya.MFileIO.newFile(True)
        globalA = 0
        globalB = 0

    def testContext(self):
        context = revl.Context(extra='extra', user='user', data='data')
        self.assertIsInstance(context.dg, OpenMaya.MDGModifier)
        self.assertIsInstance(context.dag, OpenMaya.MDagModifier)
        self.assertEqual(context.transforms, [])
        self.assertEqual(context.extra, 'extra')
        self.assertEqual(context.user, 'user')
        self.assertEqual(context.data, 'data')

    def testRun1(self):
        commands = [
            (1.0, incrementA,),
            (1.0, incrementB,),
        ]
        revl.run(commands, 123)
        self.assertTrue(globalA > 0)
        self.assertTrue(globalB > 0)
        self.assertEqual(globalA + globalB, 123)

    def testRun2(self):
        commands = [
            (1.0, incrementA,),
            (0.0, incrementB,),
        ]
        revl.run(commands, 123)
        self.assertEqual(globalA, 123)
        self.assertEqual(globalB, 0)

    def testRun3(self):
        commands = [
            (2.0, incrementA,),
            (1.0, incrementB,),
        ]
        revl.run(commands, 123)
        self.assertTrue(globalA > 0)
        self.assertTrue(globalB > 0)
        self.assertTrue(globalA > globalB)
        self.assertEqual(globalA + globalB, 123)

    def testRun4(self):
        global globalA, globalB
        commands = [
            (2.34, incrementA,),
            (1.23, incrementB,),
        ]
        aValues = []
        bValues = []
        for _ in range(123):
            globalA = 0
            globalB = 0
            revl.run(commands, 123, seed=1.23)
            aValues.append(globalA)
            bValues.append(globalB)

        self.assertTrue(all(a == globalA for a in aValues))
        self.assertTrue(all(b == globalB for b in bValues))

    def testErrorMessages(self):
        def dummy(context):
            pass

        with self.assertRaises(TypeError) as c:
            revl.run('abc', 1)

        self.assertEqual(str(c.exception), "The command set is expected to be an instance object of type 'list', or 'tuple', not 'str'.")

        with self.assertRaises(TypeError) as c:
            revl.run(['abc'], 1)

        self.assertEqual(str(c.exception), "Each command is expected to be a tuple but got 'str' instead.")

        with self.assertRaises(TypeError) as c:
            revl.run([()], 1)

        self.assertEqual(str(c.exception), "Each command is expected to be a tuple compatible with 'revl.Command' but got '()' instead.")

        with self.assertRaises(TypeError) as c:
            revl.run([('abc', dummy, (), {})], 1)

        self.assertEqual(str(c.exception), "The first element of a command, that is the 'weight' attribute, is expected to be a real number, not 'str'.")

        with self.assertRaises(TypeError) as c:
            revl.run([(1.0, 'abc', (), {})], 1)

        self.assertEqual(str(c.exception), "The second element of a command, that is the 'function' attribute, is expected to be a callable object, not 'str'.")

        with self.assertRaises(TypeError) as c:
            revl.run([(1.0, dummy, 'abc', {})], 1)

        self.assertEqual(str(c.exception), "The third element of a command, that is the 'args' attribute, is expected to be an instance object of type 'list', 'tuple', or 'NoneType', not 'str'.")

        with self.assertRaises(TypeError) as c:
            revl.run([(1.0, dummy, (), 'abc')], 1)

        self.assertEqual(str(c.exception), "The fourth element of a command, that is the 'kwargs' attribute, is expected to be an instance object of type 'dict', or 'NoneType', not 'str'.")

    def testCreateDagNode1(self):
        context = revl.Context()
        oNodes = []

        oNode = revl.createDagNode(context, 'mesh')
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kMesh))

        oNode = revl.createDagNode(context, 'parentConstraint')
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kParentConstraint))

        oNode = revl.createDagNode(context, 'pointLight')
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kPointLight))

        oNode = revl.createDagNode(context, 'renderSphere')
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kImplicitSphere))

        context.dag.doIt()
        context.dg.doIt()

        parentFullPaths = []
        dagPath = OpenMaya.MDagPath()
        for oNode in oNodes:
            OpenMaya.MDagPath.getAPathTo(oNode, dagPath)
            self.assertEqual(dagPath.length(), 2)

            dagPath.pop()
            parentFullPaths.append(dagPath.fullPathName())

        self.assertEqual(len(set(parentFullPaths)), len(parentFullPaths))

    def testCreateDagNode2(self):
        context = revl.Context()
        oNodes = []

        oRoot = revl.createTransform(context)

        oNode = revl.createDagNode(context, 'mesh', parent=True)
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kMesh))

        oNode = revl.createDagNode(context, 'parentConstraint', parent=True)
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kParentConstraint))

        oNode = revl.createDagNode(context, 'pointLight', parent=True)
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kPointLight))

        oNode = revl.createDagNode(context, 'renderSphere', parent=True)
        oNodes.append(oNode)
        self.assertTrue(oNode.hasFn(OpenMaya.MFn.kImplicitSphere))

        context.dag.doIt()
        context.dg.doIt()

        parentFullPaths = []
        dagPath = OpenMaya.MDagPath()
        for oNode in oNodes:
            OpenMaya.MDagPath.getAPathTo(oNode, dagPath)
            self.assertEqual(dagPath.length(), 2)

            dagPath.pop()
            parentFullPaths.append(dagPath.fullPathName())

        self.assertEqual(len(set(parentFullPaths)), 1)

    def testCreateDagNode3(self):
        context = revl.Context()
        self.assertEqual(revl.createDagNode(context, 'mesh', parent=True), revl.NULL_OBJ)

    def testCreateDgNode(self):
        context = revl.Context()
        self.assertTrue(revl.createDgNode(context, 'addDoubleLinear').hasFn(OpenMaya.MFn.kAddDoubleLinear))
        self.assertTrue(revl.createDgNode(context, 'bevel').hasFn(OpenMaya.MFn.kBevel))
        self.assertTrue(revl.createDgNode(context, 'clamp').hasFn(OpenMaya.MFn.kClampColor))
        self.assertTrue(revl.createDgNode(context, 'lambert').hasFn(OpenMaya.MFn.kLambert))

    def testCreatePrimitive1(self):
        context = revl.Context()
        primitive = revl.createPrimitive(context)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kCreate) or primitive.generator.hasFn(OpenMaya.MFn.kPolyPrimitive))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertTrue(len(primitive.shapes) > 0)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kGeometric) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), 1)

    def testCreatePrimitive2(self):
        context = revl.Context()
        primitives = []

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_CIRCLE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kCircle))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsCurve) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_CONE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kCone))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_CUBE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kNurbsCube))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 6)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_CYLINDER)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kCylinder))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_PLANE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kNurbsPlane))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_SPHERE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kSphere))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_SQUARE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kNurbsSquare))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 4)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsCurve) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_TORUS)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kTorus))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_CONE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyCone))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_CUBE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyCube))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_CYLINDER)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyCylinder))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_HELIX)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyHelix))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_MISC)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyPrimitiveMisc))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_PIPE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyPipe))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_PLANE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyMesh))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_PLATONIC_SOLID)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyPlatonicSolid))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_PRISM)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyPrism))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_PYRAMID)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyPyramid))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_SPHERE)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolySphere))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_TORUS)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyTorus))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        context.dag.doIt()
        context.dg.doIt()

        dagPath = OpenMaya.MDagPath()
        for primitive in primitives:
            OpenMaya.MDagPath.getAPathTo(primitive.transform, dagPath)
            self.assertEqual(dagPath.length(), 1)

    def testCreatePrimitive3(self):
        context = revl.Context()
        primitives = []

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_CUBE, name='kubo')
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kNurbsCube))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 6)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_CUBE, name='koba')
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolyCube))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives))

        context.dag.doIt()
        context.dg.doIt()

        names = ('kubo', 'koba')
        dagPath = OpenMaya.MDagPath()
        for primitive, name in zip(primitives, names):
            OpenMaya.MDagPath.getAPathTo(primitive.transform, dagPath)
            self.assertEqual(dagPath.length(), 1)
            self.assertEqual(OpenMaya.MFnTransform(primitive.transform).name(), name)

    def testCreatePrimitive4(self):
        context = revl.Context()
        primitives = []

        revl.createTransform(context)

        primitive = revl.createPrimitive(context, revl.PrimitiveType.NURBS_SPHERE, parent=True)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kSphere))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kNurbsSurface) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives) + 1)

        primitive = revl.createPrimitive(context, revl.PrimitiveType.POLY_SPHERE, parent=True)
        primitives.append(primitive)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kPolySphere))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(primitive.shapes), 1)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kMesh) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), len(primitives) + 1)

        context.dag.doIt()
        context.dg.doIt()

        dagPath = OpenMaya.MDagPath()
        for primitive in primitives:
            OpenMaya.MDagPath.getAPathTo(primitive.transform, dagPath)
            self.assertTrue(dagPath.length() > 1)

    def testCreateTransform(self):
        context = revl.Context()
        oTransforms = []

        oTransform = revl.createTransform(context)
        oTransforms.append(oTransform)
        self.assertTrue(oTransform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(context.transforms), len(oTransforms))

        oTransform = revl.createTransform(context, name='xform')
        oTransforms.append(oTransform)
        self.assertTrue(oTransform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(context.transforms), len(oTransforms))

        oTransform = revl.createTransform(context, parent=True)
        oTransforms.append(oTransform)
        self.assertTrue(oTransform.hasFn(OpenMaya.MFn.kTransform))
        self.assertEqual(len(context.transforms), len(oTransforms))

        context.dag.doIt()
        context.dg.doIt()

        names = (None, 'xform', None)
        depths = (1, 1, 2)
        dagPath = OpenMaya.MDagPath()
        for oTransform, name, depth in zip(oTransforms, names, depths):
            OpenMaya.MDagPath.getAPathTo(oTransform, dagPath)
            if name is not None:
                self.assertEqual(OpenMaya.MFnTransform(oTransform).name(), name)

            self.assertEqual(dagPath.length(), depth)

    def testUnparent(self):
        context = revl.Context()

        oRoot = revl.createTransform(context)
        oTransform = revl.createTransform(context, parent=True)

        context.transforms.remove(oRoot)
        revl.unparent(context)

        context.dag.doIt()
        context.dg.doIt()

        dagPath = OpenMaya.MDagPath()
        OpenMaya.MDagPath.getAPathTo(oTransform, dagPath)
        self.assertEqual(dagPath.length(), 1)

    def testCustomCommand(self):
        def createTemplatedPrimitive(context, type=None, name=None,
                                     parent=False):
            primitive = revl.createPrimitive(context, type=type, name=name,
                                             parent=parent)
            for oShape in primitive.shapes:
                shape = OpenMaya.MFnDependencyNode(oShape)
                context.dg.newPlugValueBool(shape.findPlug('template'), True)

            return primitive

        context = revl.Context()
        primitive = createTemplatedPrimitive(context)
        self.assertIsInstance(primitive, revl.Primitive)
        self.assertTrue(primitive.generator.hasFn(OpenMaya.MFn.kCreate) or primitive.generator.hasFn(OpenMaya.MFn.kPolyPrimitive))
        self.assertTrue(primitive.transform.hasFn(OpenMaya.MFn.kTransform))
        self.assertTrue(len(primitive.shapes) > 0)
        self.assertTrue(all(shape.hasFn(OpenMaya.MFn.kGeometric) for shape in primitive.shapes))
        self.assertEqual(len(context.transforms), 1)

        context.dag.doIt()
        context.dg.doIt()

        self.assertTrue(all(OpenMaya.MFnDependencyNode(shape).findPlug('template').asBool() == True for shape in primitive.shapes))

if __name__ == '__main__':
    unittest.main(verbosity=2)
