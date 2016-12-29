Revl
====

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


Features
--------

* generate scenes by running commands a given total number of times.
* fine control over the probability distribution for each command.
* scene generations are reproducible using a fixed seed.
* extensible with custom commands.
* fast (using Maya's API, not the command layer).


Usage
-----

.. code-block:: python

   >>> import revl
   >>> commands = [
   ...     (2.0, revl.createTransform,),
   ...     (1.0, revl.createPrimitive, (), {'parent': True})
   ... ]
   >>> count = 100
   >>> revl.run(commands, count, seed=1.23)


See the ``tutorial`` section from the documentation for more examples.


Documentation
-------------

Read the documentation online at <http://revl.readthedocs.org> or check
their source from the ``doc`` folder.

The documentation can be built in different formats using Sphinx.


Running the Tests
-----------------

A suite of unit tests is available from the ``tests`` directory. You can run it
by firing:

.. code-block:: bash

   $ mayapy tests/run.py


To run specific tests, it is possible to pass names to match in the command
line.

.. code-block:: bash

   $ mayapy tests/run.py TestCase test_my_code


This command will run all the tests within the ``TestCase`` class as well as
the individual tests which contains ``test_my_code`` in their name.


Get the Source
--------------

The source code is available from the `GitHub project page`_.


Contributing
------------

Found a bug or got a feature request? Don't keep it for yourself, log a new
issue on
`GitHub <https://github.com/christophercrouzet/revl/issues>`_.


Author
------

Christopher Crouzet
<`christophercrouzet.com <http://christophercrouzet.com>`_>


.. _GitHub project page: https://github.com/christophercrouzet/revl
