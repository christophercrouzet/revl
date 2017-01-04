.. _tests:

Running the Tests
=================

After making any code change in Revl, tests need to be evaluated to ensure that
the library still behaves as expected. These tests are available in the
``tests`` directory and can be fired through the ``test/run.py`` file:

.. code-block:: bash

   $ mayapy tests/run.py


It is possible to run specific tests by passing a space-separated list of
partial names to match:

.. code-block:: bash

   $ mayapy tests/run.py ThisTestClass and_that_function


Finally, each test file is a standalone and can be directly executed.

.. note::

   There are also benchmarks available in the ``benchmarks`` directory. They
   can be fired in the same way as described above for the tests.
