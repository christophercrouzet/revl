Revl
====

.. image:: https://img.shields.io/pypi/v/revl.svg
   :target: https://pypi.python.org/pypi/revl
   :alt: PyPI latest version

.. image:: https://readthedocs.org/projects/revl/badge/?version=latest
   :target: https://revl.readthedocs.io
   :alt: Documentation status

.. image:: https://img.shields.io/pypi/l/revl.svg
   :target: https://pypi.python.org/pypi/revl
   :alt: License


Revl helps to benchmark code for Autodesk Maya.

Upon writing a piece of code for Maya, it might be interesting to know how it
performs under different conditions, such as within scenes that are large or
small, that define a deep DAG hiearchy or a flat one, that use many node types
or only a few, and so on.

Following sets of user-provided commands, Revl can **pseudo-randomly generate
Maya scenes** with different properties against which the behaviour of a piece
of code can be observed.

The pseudo-random nature of the process can also help revealing potential bugs
by exposing edge cases that were not thought of, thus making it also a good
tool for unit testing. See `Wikipedia's Fuzzing page`_.

Note that Revl does not provide any sort of profiling tool to measure
performances. The built-in |timeit|_ module as well as other open-source
packages can be used for this purpose.


Features
--------

* generate scenes by running commands a given total number of times.
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
   ...     (1.0, revl.createPrimitive, (), {'parent': True})
   ... ]
   >>> count = 100
   >>> revl.run(commands, count, seed=1.23)


In this example, Revl is invoking a total of 100 evaluations inequally shared
between the two distinct commands provided, leading to create approximatively
80% of transforms, and 20% of primitives (also including a transform for each).
Also, the primitive type is picked randomly, and they are randomly parented
under other transforms, possibly creating a scene with a deep DAG hierarchy.

See the `Tutorial`_ section from the documentation for more information and
examples on using Revl.


Installation
------------

See the `Installation`_ section from the documentation.


Documentation
-------------

Read the documentation online at <https://revl.readthedocs.io> or check its
source in the ``doc`` directory.


Running the Tests
-----------------

Tests are available in the ``tests`` directory and can be fired through the
``run.py`` file:

.. code-block:: bash

   $ mayapy tests/run.py


It is also possible to run specific tests by passinga space-separated list of
partial names to match:

.. code-block:: bash

   $ mayapy tests/run.py TestClass


Finally, each test file is standalone and can be directly executed.


Running the Benchmarks
----------------------

Benchmarks are available in the ``benchmarks`` directory and can be fired in
the same way as described above for the tests.


Author
------

Christopher Crouzet
<`christophercrouzet.com <https://christophercrouzet.com>`_>


.. _Wikipedia's Fuzzing page: https://en.wikipedia.org/wiki/Fuzzing
.. |timeit| replace:: ``timeit``
.. _timeit: https://docs.python.org/library/timeit.html
.. _Tutorial: https://revl.readthedocs.io/en/latest/tutorial.html
.. _Installation: https://revl.readthedocs.io/en/latest/installation.html
