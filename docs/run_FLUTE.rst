run_FLUTE
=========

This page describes the script that accesses the FLUTE database.
The functions in this module ground element names and check against the FLUTE database.

Functions
---------
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

.. currentmodule:: run_FLUTE
.. autoclass:: Query
    :special-members: __init__
    :members:


Dependencies
------------

- `pandas <https://pandas.pydata.org>`_ library
- `csv <https://github.com/python/cpython/blob/3.9/Lib/csv.py>`_ module
- `numpy <https://numpy.org>`_ library
- `MySQL Connector for Python3 <https://dev.mysql.com/doc/connector-python/en/>`_ library
- `argparse <https://docs.python.org/3/library/argparse.html>`_ library
- `re <https://docs.python.org/3/library/re.html>`_ library
