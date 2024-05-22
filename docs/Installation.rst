Installation
============

MySQL Setup
-----------
1. Download the appropriate distribution of `MySQL <https://dev.mysql.com/downloads/mysql/>`_. During the installation process, you will be asked to create a local username (``root`` will be default username) and password to keep your database private.

.. Attention::
 Test your installation via typing ``mysql`` in terminal. If it's not a recognized command, you may need to permanently add it to environmental path and restart your computer. For example, in some OS, you can add via ``export PATH="/usr/local/mysql/bin:$PATH"`` in terminal

2. From the command line, access MySQL environment by typing::

	mysql -u root

   or replacing ``root`` with customized ``YOUR_USER_NAME``::
   
   	mysql -u YOUR_USER_NAME

   You can exit MySQL environment by typing ``\q``.

.. Attention::
 If the prompt fails, you may need to enter the password associated with your user account (set in step 1 during installation)::

	mysql -u root -p
 
 or::
 
 	mysql -u YOUR_USER_NAME -p
 
3. Install `MySQL Python connector <https://dev.mysql.com/doc/connector-python/en/>`_. If **pip** has been installed on your computer, use::

	pip install mysql-connector-python


FLUTE Database Creation
-----------------------

1. Download `flute.sql <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/supplementary/flute.sql.zip>`_ and unzip it as ``flute.sql``.
2. In the same directory of your downloaded copy ``flute.sql``, access MySQL environment using your username and password::

	mysql -u root -p

   and create an empty database named ``flute`` (or whatever name you prefer ``YOUR_DATABASE_NAME``)::

	CREATE DATABASE YOUR_DATABASE_NAME;
	USE YOUR_DATABASE_NAME;

   Note that ";" is required to end each MySQL command.
   
3. Type ``\q`` to log out MySQL environment, and again from the command line::

	mysql -u YOUR_USER_NAME -p YOUR_DATABASE_NAME < flute.sql

.. Note::
 You can perform the command because you are already in the same directory of your local copy ``flute.sql``, otherwise you have to specify the path to it. Also, this command aims to load the curated file ``flute.sql`` into a database named ``YOUR_DATABASE_NAME`` and store the database in your own MySQL environment. Be patient here as it may take minutes to finish loading.

4. You can now run FLUTE tool (via terminal, Jupyter notebook or GUI), you will need to specify the database name (``YOUR_DATABASE_NAME``), host name (``localhost`` for MacOS/Linux and desktop name for Windows), MySQL username (``root`` or ``YOUR_USER_NAME``) and MySQL password as arguments.

What's Inside flute.sql
-----------------------
1. Verify that ``flute.sql`` has been successfully loaded into the created database: log in MySQL environment and run ``SHOW DATABASES;``, flute should be there

.. code-block:: sql

   mysql> SHOW DATABASES;
   +--------------------+
   | Database           |
   +--------------------+
   | flute              |
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   +--------------------+
   5 rows in set (0.09 sec)


2. Enter the database via ``USE flute;``, then show all 9 tables inside this database via ``SHOW TABLES;``

.. code-block:: sql

   mysql> USE flute;
   Reading table information for completion of table and column names
   You can turn off this feature to get a quicker startup with -A
   Database changed

   mysql> SHOW TABLES;
   +------------------+
   | Tables_in_flute  |
   +------------------+
   | actions_source   |
   | biogrid          |
   | goterms          |
   | pci_detail       |
   | ppi_actions      |
   | ppi_detail_v11   |
   | protein_info     |
   | reactome         |
   | unistringmapping |
   +------------------+
   9 rows in set (0.01 sec)


3. Display first 5 rows of each table and its header via ``SELECT * FROM table_name LIMIT 5``, and get the number of rows in each table via ``SELECT COUNT(*) FROM table_name;``

.. code-block:: sql

   mysql> SELECT * FROM actions_source LIMIT 5;
   +----------+----------+------------+---------------+
   | protein1 | protein2 | mode       | sources       |
   +----------+----------+------------+---------------+
   | 10006    | 9207     | binding    | PMID028963492 |
   | 10006    | 9759     | binding    | PMID020062535 |
   | 1002293  | 994615   | binding    | PMID023717315 |
   | 10035    | 11197    | expression | PMID021488981 |
   | 10035    | 6404     | expression | PMID028553272 |
   +----------+----------+------------+---------------+
   5 rows in set (0.01 sec)

   mysql> SELECT COUNT(*) FROM actions_source;
   +----------+
   | COUNT(*) |
   +----------+
   | 10066005 |
   +----------+
   1 row in set (0.59 sec)

   mysql> SELECT * FROM biogrid LIMIT 5;
   +---------+---------+---------+--------+--------+-------+-------+------+-------+----------------------+----------------------------------------------------------------+---------------------+----------+-------------------+----------+------+------+-----------------+------------+------+------+------------+------+----------+
   | intID   | entrezA | entrezB | bIDA   | bIDB   | nameA | nameB | ogsA | ogsB  | synA                 | synB                                                           | expSys              | expSysT  | author            | PubID    | orgA | orgB | thput           | scre       | modi | phen | qual       | tg   | sourceDB |
   +---------+---------+---------+--------+--------+-------+-------+------+-------+----------------------+----------------------------------------------------------------+---------------------+----------+-------------------+----------+------+------+-----------------+------------+------+------+------------+------+----------+
   |  893309 |       1 |     368 | 106523 | 106863 | -     | -     | A1BG | ABCC6 | A1B|ABG|GAB|HYST2477 | ABC34|ARA|EST349056|GACI2|MLP1|MOAT-E|MOATE|MRP6|PXE|PXE1|URG7 | Two-hybrid          | physical | Wang J (2011)     | 21988832 | 9606 | 9606 | High Throughput | -          | -    | -    | -          | -    | BIOGRID  |
   | 2260102 |       1 |    2232 | 106523 | 108523 | -     | -     | A1BG | FDXR  | A1B|ABG|GAB|HYST2477 | ADXR                                                           | Affinity Capture-MS | physical | Huttlin EL (2017) | 28514442 | 9606 | 9606 | High Throughput | 0.88923495 | -    | -    | Quantitati | -    | BIOGRID  |
   | 2244869 |       1 |   56888 | 106523 | 121218 | -     | -     | A1BG | KCMF1 | A1B|ABG|GAB|HYST2477 | DEBT91|FIGC|PCMF|ZZZ1                                          | Affinity Capture-MS | physical | Huttlin EL (2017) | 28514442 | 9606 | 9606 | High Throughput | 0.98046280 | -    | -    | Quantitati | -    | BIOGRID  |
   |  893310 |       1 |   10549 | 106523 | 115800 | -     | -     | A1BG | PRDX4 | A1B|ABG|GAB|HYST2477 | AOE37-2|AOE372|HEL-S-97n|PRX-4                                 | Two-hybrid          | physical | Wang J (2011)     | 21988832 | 9606 | 9606 | High Throughput | -          | -    | -    | -          | -    | BIOGRID  |
   | 2238160 |       1 |   23198 | 106523 | 116807 | -     | -     | A1BG | PSME4 | A1B|ABG|GAB|HYST2477 | PA200                                                          | Affinity Capture-MS | physical | Huttlin EL (2017) | 28514442 | 9606 | 9606 | High Throughput | 0.99485253 | -    | -    | Quantitati | -    | BIOGRID  |
   +---------+---------+---------+--------+--------+-------+-------+------+-------+----------------------+----------------------------------------------------------------+---------------------+----------+-------------------+----------+------+------+-----------------+------------+------+------+------------+------+----------+
   5 rows in set (0.00 sec)

   mysql> SELECT COUNT(*) FROM biogrid;
   +----------+
   | COUNT(*) |
   +----------+
   |   344914 |
   +----------+
   1 row in set (0.04 sec)
