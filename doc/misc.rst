.. currentmodule:: revl

.. _misc:

Miscellaneous
=============

.. autosummary::
   :nosignatures:

   validate
   NULL_OBJ
   Command
   Primitive
   PrimitiveType
   pickTransform


----

.. autofunction:: validate

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
