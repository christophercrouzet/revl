.. _installation:

Installation
============

Revl requires to be run from within an `Autodesk Maya`_'s Python environment.
This is usually done either by running the code from within an interactive
session of Maya, or through using the ``mayapy`` shell. A Python interpreter is
already distributed with Maya so there is no need to install one.


Installing pip
--------------

The recommended [1]_ approach for installing a Python package such as Revl is
to use |pip|_, a package manager for projects written in Python. If ``pip`` is
not already installed on your system, you can do so by following these steps:

    1. Download |get-pip.py|_.
    2. Run ``python get-pip.py`` in a shell.


.. note::

   The installation commands described in this page might require ``sudo``
   privileges to run successfully.


System-Wide Installation
------------------------

Installing globally the most recent version of Revl can be done with ``pip``:

.. code-block:: bash

   $ pip install revl


Or using |easy_install|_ (provided with |setuptools|_):

.. code-block:: bash

   $ easy_install revl


Development Version
-------------------

To stay cutting edge with the latest development progresses, it is possible to
directly retrieve the source from the repository with the help of `Git`_:

.. code-block:: bash

   $ git clone https://github.com/christophercrouzet/revl.git
   $ cd revl
   $ pip install --editable .[dev]


.. note::

   The ``[dev]`` part installs additional dependencies required to assist
   development on Revl.

----

.. [1] See the `Python Packaging User Guide`_

.. |easy_install| replace:: ``easy_install``
.. |get-pip.py| replace:: ``get-pip.py``
.. |pip| replace:: ``pip``
.. |setuptools| replace:: ``setuptools``

.. _Autodesk Maya: http://www.autodesk.com/products/maya
.. _easy_install: https://setuptools.readthedocs.io/en/latest/easy_install.html
.. _get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
.. _Git: https://git-scm.com
.. _pip: https://pip.pypa.io
.. _Python Packaging User Guide: https://packaging.python.org/current/
.. _setuptools: https://github.com/pypa/setuptools
