.. currentmodule:: revl

.. _overview:

Overview
========

Upon writing a piece of code for Maya, it might be interesting to know how it
performs **under different conditions**, such as within scenes that are large
or small, that define a deep DAG hiearchy or a flat one, that use many node
types or only a few, and so on.

Following sets of user-provided commands, Revl can **pseudo-randomly generate
Maya scenes** with different properties against which the behaviour of a piece
of code can be observed.

The random nature of the process can also help revealing potential bugs by
exposing edge cases that were not thought of, thus making it also a good tool
for **unit testing**. See `Wikipedia's Fuzzing page`_.

Note that Revl does *not* provide any sort of profiling tool to measure
performances. The built-in |timeit|_ module as well as other open-source
packages can be used for this purpose.


Features
--------

* generates scenes by running commands a given total number of times.
* fine control over the probability distribution for each command.
* scene generations are reproducible using a fixed seed.
* extensible with custom commands.
* allows for fuzz testing.
* fast (using Maya's API, not the command layer).


Usage
-----

.. code-block:: python

   >>> import revl
   >>> commands = [
   ...     (4.0, revl.createTransform,),
   ...     (1.0, revl.createPrimitive, (), {'parent': True}),
   ... ]
   >>> count = 100
   >>> revl.run(commands, count, seed=1.23)


In this example, Revl invokes a total of 100 evaluations inequally shared
between the two distinct commands provided, leading to create approximatively
80% of transforms, and 20% of primitives (plus their associated transforms).
Also, the primitive type is picked randomly, and each primitive's transform is
randomly parented under another transform from the scene, possibly creating a
scene with a deep DAG hierarchy.

.. seealso::

   The :ref:`tutorial` section for more detailed examples and explanations on
   how to use Revl.


.. |timeit| replace:: ``timeit``

.. _timeit: https://docs.python.org/library/timeit.html
.. _Wikipedia's Fuzzing page: https://en.wikipedia.org/wiki/Fuzzing
