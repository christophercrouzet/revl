.. _installation:

Installation
============

Revl requires to be run from within an `Autodesk Maya`_'s Python environment.
This is usually done either by running the code from within an interactive
session of Maya, or through using the ``mayapy`` shell. No additional
dependency is required since a Python interpreter is already distributed with
Maya.

The recommended approach for installing a Python package such as Revl is to use
|pip|_ [1]_. If ``pip`` is not already installed on your system, you can do so
following these steps:

    1. Download |get-pip.py|_.
    2. Run ``python get-pip.py`` in a shell.


.. note::

   The installation commands described in this page might require ``sudo``
   privileges to run successfully.


System-Wide Installation
------------------------

Installing globally the most recent version of Revl can be done with |pip|_:

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
   $ python setup.py develop

----

.. [1] See the `Python Packaging User Guide`_


.. |easy_install| replace:: ``easy_install``
.. |get-pip.py| replace:: ``get-pip.py``
.. |pip| replace:: ``pip``
.. |setuptools| replace:: ``setuptools``


.. _Autodesk Maya: http://www.autodesk.com/products/maya
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _get-pip.py: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
.. _Git: https://git-scm.com
.. _pip: https://pypi.python.org/pypi/pip
.. _Python Packaging User Guide: https://python-packaging-user-guide.readthedocs.io
.. _setuptools: https://pypi.python.org/pypi/setuptools
