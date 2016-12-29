.. currentmodule:: revl

.. _overview:

Overview
========

Revl helps to benchmark code for Autodesk Maya.

Upon writing a piece of code for Maya, it might be interesting to know how it
performs under different conditions, such as within scenes that are large or
small, that define a deep DAG hiearchy or a flat one, that use many node types
or only a few, and so on.

Following sets of user-provided commands, Revl can pseudo-randomly generate
Maya scenes with different properties against which the behaviour of a piece of
code can be observed.

The pseudo-random nature of the process can also help revealing potential bugs
by exposing edge cases that were not thought of, thus making it also a good
tool for unit testing.


.. seealso::

   A description of the usage of Revl as well as a few examples are available
   in the :ref:`tutorial` section.
