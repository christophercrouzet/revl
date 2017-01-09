.. currentmodule:: revl

.. _misc:

Miscellaneous
=============

.. autosummary::
   :nosignatures:

   NULL_OBJ
   Command
   Primitive
   PrimitiveType
   pickTransform


----

.. autodata:: NULL_OBJ

   Constant denoting an invalid object.

----

.. autoclass:: Command(weight, function, args=None, kwargs=None)

----

.. autoclass:: Primitive(generator, transform, shapes)

----

.. autoclass:: PrimitiveType

----

.. autofunction:: pickTransform
