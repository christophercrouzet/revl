#                      __
#   .----.-----.--.--.|  |
#   |   _|  -__|  |  ||  |
#   |__| |_____|\___/ |__|
#

"""
    revl
    ~~~~

    Helps to benchmark code for Autodesk Maya.

    :copyright: Copyright 2016-2017 by Christopher Crouzet.
    :license: MIT, see LICENSE for details.
"""

import collections
import numbers
import random
import sys

from maya import OpenMaya


__version__ = '0.2.0'


if sys.version_info[0] == 2:
    _BUILTIN_MODULE = '__builtin__'

    def _iteritems(d, **kwargs):
        return d.iteritems(**kwargs)

    _range = xrange
else:
    _BUILTIN_MODULE = 'builtins'

    def _iteritems(d, **kwargs):
        return iter(d.items(**kwargs))

    _range = range

_SEQUENCE_TYPES = (list, tuple)


#: Constant denoting an invalid object.
NULL_OBJ = OpenMaya.MObject().kNullObj


class Context(object):

    """Evaluation context.

    Each command function needs to define this context as first parameter.

    Attributes
    ----------
    dg : maya.OpenMaya.MDGModifier
        DG modifier.
    dag : maya.OpenMaya.MDagModifier
        DAG modifier.
    transforms : list of maya.OpenMaya.MObject
        Transform nodes. Provides data for the :func:`pickTransform` function.
    """

    def __init__(self, **kwargs):
        """Constructor.

        Parameters
        ----------
        kwargs
            Keyword arguments to define additional attributes.
        """
        self.dg = OpenMaya.MDGModifier()
        self.dag = OpenMaya.MDagModifier()
        self.transforms = []
        self.__dict__.update(kwargs)

    def __repr__(self):
        values = ', '.join(['%s=%r' % (k, v)
                            for k, v in sorted(_iteritems(self.__dict__))])
        return "%s(%s)" % (type(self).__name__, values)


_Command = collections.namedtuple(
    'Command', (
        'weight',
        'function',
        'args',
        'kwargs',
    ))
_Command.__new__.__defaults__ = (None, None)


class Command(_Command):

    """Weighted command.

    It is not necessary to use this class to define a command as it can be done
    by directly using a tuple instead. But the tuple needs to be compatible
    with the structure defined here.

    Attributes
    ----------
    weight : float
        Probability for this command to be evaluated. The value is relative
        to the other commands defined in the same set.
    function : function
        Function to evaluate. Its first argument needs to the command context
        :class:`Context`.
    args : tuple or None
        Additional arguments to pass to the function. ``None`` is the
        equivalent of setting an empty tuple.
    kwargs : dict or None
        Keyword arguments to pass to the function. ``None`` is the equivalent
        of setting an empty dictionary.
    """

    __slots__ = ()


_COMMAND_ATTR_COUNT = len(Command._fields)
_COMMAND_REQUIRED_ARG_RANGE = _range(
    _COMMAND_ATTR_COUNT - len(Command.__new__.__defaults__),
    _COMMAND_ATTR_COUNT + 1)


_Primitive = collections.namedtuple(
    'Primitive', (
        'generator',
        'transform',
        'shapes',
    ))


class Primitive(_Primitive):

    """Primitive.

    An instance of this class is returned by the :func:`createPrimitive`
    function.

    Attributes
    ----------
    generator : maya.OpenMaya.MObject
        Node object generating the shapes.
    transform : maya.OpenMaya.MObject
        Transform object.
    shapes : list of maya.OpenMaya.MObject
        Shape objects.
    """

    __slots__ = ()


class PrimitiveType(object):

    """Enumerator for the primitive types.

    This is used as a parameter for the :func:`createPrimitive` function.

    Attributes
    ----------
    NURBS_CIRCLE
    NURBS_CONE
    NURBS_CUBE
    NURBS_CYLINDER
    NURBS_PLANE
    NURBS_SPHERE
    NURBS_SQUARE
    NURBS_TORUS
    POLY_CONE
    POLY_CUBE
    POLY_CYLINDER
    POLY_HELIX
    POLY_MISC
    POLY_PIPE
    POLY_PLANE
    POLY_PLATONIC_SOLID
    POLY_PRISM
    POLY_PYRAMID
    POLY_SPHERE
    POLY_TORUS
    """

    NURBS_CIRCLE = 0
    NURBS_CONE = 1
    NURBS_CUBE = 2
    NURBS_CYLINDER = 3
    NURBS_PLANE = 4
    NURBS_SPHERE = 5
    NURBS_SQUARE = 6
    NURBS_TORUS = 7
    POLY_CONE = 8
    POLY_CUBE = 9
    POLY_CYLINDER = 10
    POLY_HELIX = 11
    POLY_MISC = 12
    POLY_PIPE = 13
    POLY_PLANE = 14
    POLY_PLATONIC_SOLID = 15
    POLY_PRISM = 16
    POLY_PYRAMID = 17
    POLY_SPHERE = 18
    POLY_TORUS = 19

    _FIRST = NURBS_CIRCLE
    _LAST = POLY_TORUS


_PrimitiveTraits = collections.namedtuple(
    '_PrimitiveTraits', (
        'type',
        'shapeType',
        'outPlugs',
        'inPlug',
    ))


def _defineCurveTraits(type, outPlugs=None):
    outPlugs = ['outputCurve'] if outPlugs is None else outPlugs
    return _PrimitiveTraits(type=type, shapeType='nurbsCurve',
                            outPlugs=outPlugs, inPlug='create')


def _defineMeshTraits(type):
    return _PrimitiveTraits(type=type, shapeType='mesh', outPlugs=['output'],
                            inPlug='inMesh')


def _defineSurfaceTraits(type, outPlugs=None):
    outPlugs = ['outputSurface'] if outPlugs is None else outPlugs
    return _PrimitiveTraits(type=type, shapeType='nurbsSurface',
                            outPlugs=outPlugs, inPlug='create')


_PRIMITIVE_TRAITS = {
    PrimitiveType.NURBS_CIRCLE: _defineCurveTraits('makeNurbCircle'),
    PrimitiveType.NURBS_CONE: _defineSurfaceTraits('makeNurbCone'),
    PrimitiveType.NURBS_CUBE: _defineSurfaceTraits(
        'makeNurbCube', outPlugs=['outputSurface%s' % (i if i > 0 else '',)
                                  for i in _range(6)]),
    PrimitiveType.NURBS_CYLINDER: _defineSurfaceTraits('makeNurbCylinder'),
    PrimitiveType.NURBS_PLANE: _defineSurfaceTraits('makeNurbPlane'),
    PrimitiveType.NURBS_SPHERE: _defineSurfaceTraits('makeNurbSphere'),
    PrimitiveType.NURBS_SQUARE: _defineCurveTraits(
        'makeNurbsSquare', outPlugs=['outputCurve%s' % (i,)
                                     for i in _range(1, 5)]),
    PrimitiveType.NURBS_TORUS: _defineSurfaceTraits('makeNurbTorus'),
    PrimitiveType.POLY_CONE: _defineMeshTraits('polyCone'),
    PrimitiveType.POLY_CUBE: _defineMeshTraits('polyCube'),
    PrimitiveType.POLY_HELIX: _defineMeshTraits('polyHelix'),
    PrimitiveType.POLY_CYLINDER: _defineMeshTraits('polyCylinder'),
    PrimitiveType.POLY_MISC: _defineMeshTraits('polyPrimitiveMisc'),
    PrimitiveType.POLY_PIPE: _defineMeshTraits('polyPipe'),
    PrimitiveType.POLY_PLANE: _defineMeshTraits('polyPlane'),
    PrimitiveType.POLY_PLATONIC_SOLID: _defineMeshTraits('polyPlatonicSolid'),
    PrimitiveType.POLY_PRISM: _defineMeshTraits('polyPrism'),
    PrimitiveType.POLY_PYRAMID: _defineMeshTraits('polyPyramid'),
    PrimitiveType.POLY_SPHERE: _defineMeshTraits('polySphere'),
    PrimitiveType.POLY_TORUS: _defineMeshTraits('polyTorus'),
}


def validate(commands):
    """Check if the commands are well-formed.

    Parameters
    ----------
    commands : list of revl.Command or compatible tuple
        Commands.

    Raises
    ------
    TypeError
        Some of the commands aren't well-formed.
    """
    # The following checks are not to enforce some sort of type checking
    # in place of Python's duck typing but rather to give a chance to provide
    # more meaningful error messages to the user.

    if not isinstance(commands, _SEQUENCE_TYPES):
        raise TypeError(
            "The command set is expected to be an instance object of type %s, "
            "not '%s'." % (_joinTypes(_SEQUENCE_TYPES, "or "),
                           _formatType(type(commands)),))

    # Check the overall shape of each command.
    for command in commands:
        if not isinstance(command, _SEQUENCE_TYPES):
            raise TypeError(
                "Each command is expected to be an instance object of type "
                "%s, not '%s'."
                % (_joinTypes(_SEQUENCE_TYPES + (Command,), "or "),
                   _formatType(type(command)),))

        if len(command) not in _COMMAND_REQUIRED_ARG_RANGE:
            raise TypeError(
                "Each command is expected to be an instance object of type "
                "%s, and compatible with the '%s' structure, but got '%s' "
                "instead." % (_joinTypes(_SEQUENCE_TYPES + (Command,), "or "),
                              _formatType(Command), command))

    # Check each command attribute.
    for command in commands:
        command = Command(*command)
        if not isinstance(command.weight, numbers.Real):
            raise TypeError(
                "The first element of a command, that is the 'weight' "
                "attribute, is expected to be a real number, not '%s'."
                % (_formatType(type(command.weight))))

        if not callable(command.function):
            raise TypeError(
                "The second element of a command, that is the 'function' "
                "attribute, is expected to be a callable object, not '%s'."
                % (_formatType(type(command.function))))

        if (command.args is not None
                and not isinstance(command.args, _SEQUENCE_TYPES)):
            raise TypeError(
                "The third element of a command, that is the 'args' "
                "attribute, is expected to be an instance object of type %s, "
                "not '%s'."
                % (_joinTypes(_SEQUENCE_TYPES + (type(None),), "or "),
                   _formatType(type(command.args))))

        if (command.kwargs is not None
                and not isinstance(command.kwargs, dict)):
            raise TypeError(
                "The fourth element of a command, that is the 'kwargs' "
                "attribute, is expected to be an instance object of type "
                "'dict', or 'NoneType', not '%s'."
                % (_formatType(type(command.kwargs))))

    return True


def run(commands, count, seed=None, context=None):
    """Randomly run weighted commands from a set.

    Each command comes with a weight which determines the probabilities for
    that command to be run.

    Use :func:`validate` to check if the input command set is well-formed.

    Parameters
    ----------
    commands : list of revl.Command or compatible tuple
        Set of weighted commands.
    count : int
        Total number of commands to be run. Setting a count greater than the
        number of weighted commands doesn't guarantee that each command will
        be run once. Some might be run multiple times instead.
    seed : object
        Hashable object to define the starting seed of the pseudo-random
        number generations. If ``None``, the current system time is used.
        Running multiple times a same set of commands with a same fixed seed
        that is not ``None`` produces identitcal results.
    context : revl.Context
        Context to use. If ``None``, a new one is created.

    Returns
    -------
    revl.Context
        The context after evaluating the commands.

    Examples
    --------
    >>> import revl
    >>> commands = [
    ...     (2.0, revl.createTransform,),
    ...     (1.0, revl.createPrimitive, (), {'parent': True})
    ... ]
    >>> revl.run(commands, 100, seed=1.23)
    """
    random.seed(seed)
    commands = _consolidate(commands)

    if context is None:
        context = Context()

    commands = [c for c in commands if c.weight > 0]
    if commands:
        for command in _pick(commands, count):
            args = () if command.args is None else command.args
            kwargs = {} if command.kwargs is None else command.kwargs
            command.function(context, *args, **kwargs)

    context.dag.doIt()
    context.dg.doIt()
    return context


def pickTransform(context):
    """Randomly pick a transform.

    Pickable transforms are listed within the :attr:`Context.transforms`
    attribute.

    Parameters
    ----------
    context : revl.Context
        Command context.

    Returns
    -------
    maya.OpenMaya.MObject
        The picked transform or :const:`NULL_OBJ` if the attribute
        :attr:`Context.transforms` is empty.
    """
    if not context.transforms:
        return NULL_OBJ

    return context.transforms[random.randint(0, len(context.transforms) - 1)]


def createDagNode(context, type, parent=False):
    """Create a DAG node.

    To create a transform node or a geometry primitive, respectively use the
    functions :func:`createTransform` or :func:`createPrimitive`.

    Parameters
    ----------
    context : revl.Context
        Command context.
    type : maya.OpenMaya.MTypeId or str
        Type of the node to create, for example: 'mesh', 'parentConstraint',
        'pointLight', 'renderSphere', and so on.
    parent : bool
        ``True`` to parent the new DAG node under a transform randomly picked
        from the scene. If ``True`` but no transform could be found in the
        scene, then the DAG node isn't created. If ``False``, a new transform
        is always created at the world and is used as the parent for the new
        DAG node.

    Returns
    -------
    maya.OpenMaya.MObject
        The new node object or :const:`NULL_OBJ` if the parameter 'parent' was
        set to ``True`` but no transform could be found.
    """
    if parent:
        oParent = pickTransform(context)
        if oParent is NULL_OBJ:
            return NULL_OBJ
    else:
        oParent = context.dag.createNode('transform')
        context.transforms.append(oParent)

    return context.dag.createNode(type, oParent)


def createDgNode(context, type):
    """Create a DG node.

    To create a DAG node, use either one of the functions
    :func:`createDagNode`, :func:`createTransform`, or :func:`createPrimitive`.

    Parameters
    ----------
    context : revl.Context
        Command context.
    type : maya.OpenMaya.MTypeId or str
        Type of the node to create, for example: 'addDoubleLinear', 'bevel',
        'clamp', 'lambert', and so on.

    Returns
    -------
    maya.OpenMaya.MObject
        The new node object.
    """
    return context.dg.createNode(type)


def createPrimitive(context, type=None, name=None, parent=False,
                    forceTransformCreation=True):
    """Create a geometry primitive.

    Parameters
    ----------
    context : revl.Context
        Command context.
    type : int
        Primitive type. Available values are enumerated in the
        :class:`PrimitiveType` class. If ``None``, a primitive type is randomly
        picked.
    name : str
        Base name for the new transform node. If ``None``, no name is
        explicitely set.
    parent : bool
        ``True`` to parent the new transform under another transform randomly
        picked from the scene, if any. Otherwise it is parented under the
        world.
    forceTransformCreation : bool
        ``True`` to always create a new transform with the shapes as child,
        otherwise a new transform is created only if the parameter ``parent``
        is ``False`` or if no transform could be found in the scene to parent
        the shapes to.

    Returns
    -------
    revl.Primitive
        The new primitive, that is its generator, its transform, and its
        shapes.
    """
    if type is None:
        type = random.randint(PrimitiveType._FIRST, PrimitiveType._LAST)

    oParent = pickTransform(context) if parent else NULL_OBJ
    if forceTransformCreation or oParent is NULL_OBJ:
        oTransform = context.dag.createNode('transform', oParent)
        context.transforms.append(oTransform)
    else:
        oTransform = oParent

    traits = _PRIMITIVE_TRAITS[type]
    oGenerator = context.dg.createNode(traits.type)
    generator = OpenMaya.MFnDependencyNode(oGenerator)

    shapes = []
    for outPlug in traits.outPlugs:
        oShape = context.dag.createNode(traits.shapeType, oTransform)
        shape = OpenMaya.MFnDagNode(oShape)
        context.dg.connect(generator.findPlug(outPlug),
                           shape.findPlug(traits.inPlug))
        shapes.append(oShape)

    if name is not None:
        OpenMaya.MFnDagNode(oTransform).setName(name)

    return Primitive(generator=oGenerator, transform=oTransform, shapes=shapes)


def createTransform(context, name=None, parent=False):
    """Create a transform node.

    Parameters
    ----------
    context : revl.Context
        Command context.
    name : str
        Name of the new transform node. If ``None``, the default name is used.
    parent : bool
        ``True`` to parent the new transform under another transform randomly
        picked from the scene, if any. Otherwise it is parented under the
        world.

    Returns
    -------
    maya.OpenMaya.MObject
        The new transform object.
    """
    oParent = pickTransform(context) if parent else NULL_OBJ
    oTransform = context.dag.createNode('transform', oParent)
    if name is not None:
        OpenMaya.MFnDagNode(oTransform).setName(name)

    context.transforms.append(oTransform)
    return oTransform


def unparent(context):
    """Unparent a random transform node.

    Parameters
    ----------
    context : revl.Context
        Command context.
    """
    oNode = pickTransform(context)
    if oNode is NULL_OBJ:
        return

    context.dag.reparentNode(oNode, NULL_OBJ)


def _consolidate(commands):
    """Enforce the structure of the commands.

    Parameters
    ----------
    commands : list of revl.Command or compatible tuple
        Commands.

    Returns
    -------
    list of revl.Command
        The consolidated commands.
    """
    return [Command(*c) for c in commands]


def _pick(commands, count):
    """Randomly pick commands from a set a given number of times.

    Parameters
    ----------
    commands : list of revl.Command
        Set of weighted commands available for picking.
    count : int
        Total number of commands to pick.

    Yields
    ------
    revl.Command
        The command picked.
    """
    # Credits: Ned Batchelder for his answer on StackOverflow at
    # http://stackoverflow.com/a/3679747/1640404.
    total = sum(c.weight for c in commands)
    for _ in _range(count):
        r = random.uniform(0, total)
        v = 0
        for command in commands:
            v += command.weight
            if v >= r:
                yield command
                break


def _formatType(cls):
    """Format a type name for printing.

    Parameters
    ----------
    cls : type
        Class object.

    Returns
    -------
    str
        The formatted class object name.
    """
    if cls.__module__ == _BUILTIN_MODULE:
        return cls.__name__
    else:
        return '%s.%s' % (cls.__module__, cls.__name__)


def _formatElement(element, count, index, lastSeparator):
    """Format an element from a sequence.

    This only prepends a separator for the last element and wraps each element
    with single quotes.

    Parameters
    ----------
    element : object
        Current element.
    count : int
        Total number of items in the sequence.
    index : int
        Current index.
    lastSeparator : str
        Separator to be used for joining the last element when multiple
        elements are to be joined.

    Returns
    -------
    str
        The joined object string representations.
    """
    return ("%s'%s'" % (lastSeparator, element)
            if count > 1 and index == count - 1
            else "'%s'" % (element,))


def _joinSequence(seq, lastSeparator=''):
    """Join a sequence into a string.

    Parameters
    ----------
    seq : sequence
        Object string representations to be joined.
    lastSeparator : str
        Separator to be used for joining the last element when multiple
        elements are to be joined.

    Returns
    -------
    str
        The joined object string representations.
    """
    count = len(seq)
    return ', '.join(_formatElement(element, count, i, lastSeparator)
                     for i, element in enumerate(seq))


def _joinTypes(seq, lastSeparator=''):
    """Join class object names into a string.

    Parameters
    ----------
    seq : sequence
        Class objects whose names are to be joined.
    lastSeparator : str
        Separator to be used for joining the last element when multiple types
        are to be joined.

    Returns
    -------
    str
        The joined class object names.
    """
    classNames = [_formatType(cls) for cls in seq]
    return _joinSequence(classNames, lastSeparator)
