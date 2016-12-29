.. currentmodule:: revl

.. _tutorial:

Tutorial
========

Revl is all about :ref:`generating pseudo-random Maya scenes <generate_scene>`
by evaluating a set of weighted commands.

The built-in commands are fairly basic and might not cover all your needs, in
which case you are encouraged to :ref:`provide your own <write_command>`.


.. _generate_scene:

Generating a Scene
------------------

A scene can be generated in two steps: creating a set of weighted commands, and
evaluating it.

Each weighted command can be defined either by using the class :class:`Command`
or by using a tuple that follows the same structure than the :class:`Command`
class. Indeed, all the command definitions below are equal:

.. code-block:: python

   >>> import revl
   >>> command1 = revl.Command(weight=1.0, function=revl.createTransform)
   >>> command2 = revl.Command(1.0, revl.createTransform)
   >>> command3 = (1.0, revl.createTransform)


The :ref:`command functions <command_functions>` being evaluated later on, any
argument also needs to be passed to a command definition:

.. code-block:: python

   >>> import revl
   >>> command1 = revl.Command(weight=1.0, function=revl.createTransform,
   ...                         args=(), kwargs={'parent': True})
   >>> command2 = revl.Command(1.0, revl.createTransform, (), {'parent': True})
   >>> command3 = (1.0, revl.createTransform, (), {'parent': True})


From there, actually generating a scene is only a matter of adding the commands
in a list and calling the :func:`run` function:

.. code-block:: python

   >>> import revl
   >>> commands = [
   ...     (1.0, revl.createTransform),
   ... ]
   >>> revl.run(commands, 100)


This example creates a scene with 100 transform nodes parented to the world.
Setting the :func:`createTransform` function's parameter ``parent`` to ``True``
like before, already helps with adding a bit of randomness into the result:

.. code-block:: python

   >>> import revl
   >>> commands = [
   ...     (1.0, revl.createTransform, (), {'parent': True}),
   ... ]
   >>> revl.run(commands, 100)


The 100 transform nodes are now randomly parented under other transforms. The
:attr:`Command.weight` attribute has no effect here, so let's see it in action:

.. code-block:: python

   >>> import revl
   >>> Type = revl.PrimitiveType
   >>> commands = [
   ...     (1.0, revl.createPrimitive, (), {'type': Type.POLY_CONE}),
   ...     (2.0, revl.createPrimitive, (), {'type': Type.POLY_CUBE}),
   ...     (5.0, revl.createPrimitive, (), {'type': Type.POLY_SPHERE}),
   ... ]
   >>> revl.run(commands, 100)


Revl is running here a total of 100 command evaluations inequally shared
between the three distinct commands provided, leading the resulting scene to
contain approximatively 12.5% of cones, 25% of cubes, and 62.5% of spheres.


.. _write_command:

Writing a Custom Command
------------------------

The built-in commands don't offer much features. Instead they aim to be simple
and fast, and as such are good contenders to be used as building blocks to
compose more advanced commands.

For example, it is possible to extend the function :func:`createPrimitive` to
set the resulting shapes as templates:

.. code-block:: python

   >>> import revl
   >>> def createTemplatedPrimitive(context, type=None, name=None,
   ...                              parent=False):
   ...     primitive = revl.createPrimitive(context, type=type, name=name,
   ...                                      parent=parent)
   ...     for oShape in primitive.shapes:
   ...         shape = OpenMaya.MFnDependencyNode(oShape)
   ...         context.dg.newPlugValueBool(shape.findPlug('template'), True)
   ...     return primitive
   >>> commands = [
   ...     (1.0, revl.createPrimitive),
   ...     (1.0, createTemplatedPrimitive),
   ... ]
   >>> revl.run(commands, 100)


This example will generate a scene with as much normal primitives than
templated ones.

.. note::

   When creating a new transform node, append the resulting ``maya.MObject``
   object to the :attr:`Context.transforms` list attribute. This will allow
   the function :func:`pickTransform` to have more transform nodes to pick
   from.


.. note::

   For performance reasons, you are encouraged to make use of the
   :attr:`Context.dg` and :attr:`Context.dag` attributes. This buffers the DG
   and DAG operations, and applies them at the end of the :func:`run` function.

   If a custom command needs to access certain features requiring the graphs
   to be up-to-date, then feel free to call their ``doIt()`` methods.
