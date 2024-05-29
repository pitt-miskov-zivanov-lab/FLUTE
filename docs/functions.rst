Functions in FLUTE
==================

This page describes the functions supported in FLUTE tool, including general functions that run without accessing database, and query functions that access the ``flute.sql`` database.


General Functions
-----------------
.. currentmodule:: run_FLUTE
.. autofunction:: filter_protein_ints

.. currentmodule:: run_FLUTE
.. autofunction:: get_chem_id

.. currentmodule:: run_FLUTE
.. autofunction:: get_go_id

.. currentmodule:: run_FLUTE
.. autofunction:: get_string_id

.. currentmodule:: run_FLUTE
.. autofunction:: get_uid

.. currentmodule:: run_FLUTE
.. autofunction:: extract_year

.. currentmodule:: run_FLUTE
.. autofunction:: filter_recent_ints

.. currentmodule:: run_FLUTE
.. autofunction:: get_duplicates_ints

Query Functions
---------------
.. currentmodule:: run_FLUTE
.. autoclass:: Query
    :special-members: __init__
    :members:


Dependencies
------------

- `pandas <https://pandas.pydata.org>`_ library
- `numpy <https://numpy.org>`_ library
- `matplotlib <https://matplotlib.org>`_ library
- `networkx <https://networkx.org>`_ library
- `MySQL Connector for Python3 <https://dev.mysql.com/doc/connector-python/en/>`_ library
