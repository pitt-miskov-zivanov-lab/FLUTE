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

   mysql> SELECT * FROM goterms LIMIT 5;
   +-----------+------------+---------------+------------+----------------+----------+---------------------------+----------+----------------------------------------------------+---------------------------+---------+------------+----------+------------+
   | db1       | id1        | unknown1      | goterm     | ref            | evidence | pfam                      | unknown2 | name                                               | lbl                       | type    | taxon      | date     | db2        |
   +-----------+------------+---------------+------------+----------------+----------+---------------------------+----------+----------------------------------------------------+---------------------------+---------+------------+----------+------------+
   | UniProtKB | A0A024R161 | DNAJC25-GNG10 | GO:0003924 | GO_REF:0000002 | IEA      | InterPro:IPR001770        | F        | Guanine nucleotide-binding protein subunit gamma   | DNAJC25-GNG10|hCG_1994888 | protein | taxon:9606 | 20190112 | InterPro   |
   | UniProtKB | A0A024R161 | DNAJC25-GNG10 | GO:0005515 | PMID:21873635  | IBA      | PANTHER:PTN002492804|UniP | F        | Guanine nucleotide-binding protein subunit gamma   | DNAJC25-GNG10|hCG_1994888 | protein | taxon:9606 | 20180425 | GO_Central |
   | UniProtKB | A0A024R161 | DNAJC25-GNG10 | GO:0005834 | PMID:21873635  | IBA      | FB:FBgn0004921|PANTHER:PT | C        | Guanine nucleotide-binding protein subunit gamma   | DNAJC25-GNG10|hCG_1994888 | protein | taxon:9606 | 20180425 | GO_Central |
   | UniProtKB | A0A024R161 | DNAJC25-GNG10 | GO:0007186 | GO_REF:0000002 | IEA      | InterPro:IPR001770|InterP | P        | Guanine nucleotide-binding protein subunit gamma   | DNAJC25-GNG10|hCG_1994888 | protein | taxon:9606 | 20190112 | InterPro   |
   | UniProtKB | A0A024RBG1 | NUDT4B        | GO:0003723 | GO_REF:0000037 | IEA      | UniProtKB-KW:KW-0694      | F        | Diphosphoinositol polyphosphate phosphohydrolase N | NUDT4B                    | protein | taxon:9606 | 20190112 | UniProt    |
   +-----------+------------+---------------+------------+----------------+----------+---------------------------+----------+----------------------------------------------------+---------------------------+---------+------------+----------+------------+
   5 rows in set (0.03 sec)

   mysql> SELECT COUNT(*) FROM goterms;
   +----------+
   | COUNT(*) |
   +----------+
   |   279924 |
   +----------+
   1 row in set (0.20 sec)

   mysql> SELECT * FROM pci_detail LIMIT 5;
   +--------------+----------------------+------+------+------+------+-------+
   | chem         | prot                 | exp  | pred | data | text | score |
   +--------------+----------------------+------+------+------+------+-------+
   | CIDm00000040 | 9606.ENSP00000000233 |    0 |    0 |    0 |  177 |   177 |
   | CIDm00000174 | 9606.ENSP00000000233 |  675 |    0 |    0 |    0 |   675 |
   | CIDm00000197 | 9606.ENSP00000000233 |    0 |    0 |    0 |  193 |   193 |
   | CIDm00000205 | 9606.ENSP00000000233 |    0 |    0 |    0 |  179 |   179 |
   | CIDm00000237 | 9606.ENSP00000000233 |    0 |    0 |    0 |  164 |   164 |
   +--------------+----------------------+------+------+------+------+-------+
   5 rows in set (0.00 sec)

   mysql> SELECT COUNT(*) FROM pci_detail;
   +----------+
   | COUNT(*) |
   +----------+
   | 15473939 |
   +----------+
   1 row in set (1.56 sec)

   mysql> SELECT * FROM ppi_actions LIMIT 5;
   +----------------------+----------------------+----------+--------+-----------+--------+-------+
   | protein1             | protein2             | mode     | action | direction | acting | score |
   +----------------------+----------------------+----------+--------+-----------+--------+-------+
   | item_id_a            | item_id_b            | mode     | action | i         | a      |     0 |
   | 9606.ENSP00000000233 | 9606.ENSP00000216366 | binding  |        | f         | f      |   165 |
   | 9606.ENSP00000000233 | 9606.ENSP00000216366 | reaction |        | f         | f      |   165 |
   | 9606.ENSP00000000233 | 9606.ENSP00000216366 | reaction |        | t         | f      |   165 |
   | 9606.ENSP00000000233 | 9606.ENSP00000216366 | reaction |        | t         | t      |   165 |
   +----------------------+----------------------+----------+--------+-----------+--------+-------+
   5 rows in set (0.04 sec)

   mysql> SELECT COUNT(*) FROM ppi_actions;
   +----------+
   | COUNT(*) |
   +----------+
   |  3470907 |
   +----------+
   1 row in set (0.47 sec)

   mysql> SELECT * FROM ppi_detail_v11 LIMIT 5;
   +----------------------+----------------------+--------+--------+--------+--------+--------+--------+--------+
   | protein1             | protein2             | nscore | fscore | cscore | ascore | escore | dscore | tscore |
   +----------------------+----------------------+--------+--------+--------+--------+--------+--------+--------+
   | 9606.ENSP00000000233 | 9606.ENSP00000000412 |      0 |      0 |      0 |    101 |      0 |      0 |    105 |
   | 9606.ENSP00000000233 | 9606.ENSP00000003100 |      0 |      0 |      0 |     55 |     85 |      0 |    166 |
   | 9606.ENSP00000000233 | 9606.ENSP00000005260 |      0 |      0 |      0 |      0 |    262 |      0 |      0 |
   | 9606.ENSP00000000233 | 9606.ENSP00000007414 |      0 |      0 |      0 |     51 |     83 |      0 |    108 |
   | 9606.ENSP00000000233 | 9606.ENSP00000009105 |      0 |      0 |      0 |     62 |    167 |      0 |     56 |
   +----------------------+----------------------+--------+--------+--------+--------+--------+--------+--------+
   5 rows in set (0.02 sec)

   mysql> SELECT COUNT(*) FROM ppi_detail_v11;
   +----------+
   | COUNT(*) |
   +----------+
   | 11759454 |
   +----------+
   1 row in set (1.72 sec)

   mysql> SELECT * FROM protein_info LIMIT 5;
   +-------------+---------------------+------------+---------------------------+
   | internal_id | external_id         | species_id | pref_name                 |
   +-------------+---------------------+------------+---------------------------+
   | 10000       | 287.DR97_4286       | 287        | frr                       |
   | 100000      | 991.IW20_09805      | 991        | IW20_09805                |
   | 1000000     | 3988.XP_002516123.1 | 3988       |  putative; Encoded by tra |
   | 10000000    | 140110.NechaP73009  | 140110     | NechaP73009               |
   | 10000001    | 140110.NechaP7302   | 140110     | NechaP7302                |
   +-------------+---------------------+------------+---------------------------+
   5 rows in set (0.00 sec)

   mysql> SELECT COUNT(*) FROM protein_info;
   +----------+
   | COUNT(*) |
   +----------+
   | 24584629 |
   +----------+
   1 row in set (2.76 sec)

   mysql> SELECT * FROM reactome LIMIT 5;
   +------------+------------------+----------------------+------------------------+-------------------------------------+
   | upID1      | upID2            | intType              | context                | ref                                 |
   +------------+------------------+----------------------+------------------------+-------------------------------------+
   | ChEBI:1294 | uniprotkb:P05108 | physical association | reactome:R-HSA-5580269 | 21636783|15507506|11502818|21159840 |
   | ChEBI:1294 | uniprotkb:P05108 | physical association | reactome:R-HSA-193101  | 3024157|21636783|9578606            |
   | ChEBI:1294 | uniprotkb:P10109 | physical association | reactome:R-HSA-5580269 | 21636783|15507506|11502818|21159840 |
   | ChEBI:1294 | uniprotkb:P10109 | physical association | reactome:R-HSA-193101  | 3024157|21636783|9578606            |
   | ChEBI:1294 | uniprotkb:P22570 | physical association | reactome:R-HSA-5580269 | 21636783|15507506|11502818|21159840 |
   +------------+------------------+----------------------+------------------------+-------------------------------------+
   5 rows in set (0.01 sec)

   mysql> SELECT COUNT(*) FROM reactome;
   +----------+
   | COUNT(*) |
   +----------+
   |    61230 |
   +----------+
   1 row in set (0.04 sec)

   mysql> SELECT * FROM unistringmapping LIMIT 5;
   +------------+------------+----------------------+------+------+
   | uniID      | ogs        | stringID             | conf | unk  |
   +------------+------------+----------------------+------+------+
   | A0A024R161 | A0A024R161 | 9606.ENSP00000363412 |  100 |  305 |
   | A0A075B734 | A0A075B734 | 9606.ENSP00000456868 |  100 |  710 |
   | A0A075B759 | PAL4E      | 9606.ENSP00000485638 |  100 |  339 |
   | A0A075B762 | A0A075B762 | 9606.ENSP00000463957 |   98 | 7270 |
   | A0A075B767 | A0A075B767 | 9606.ENSP00000464619 |  100 |  340 |
   +------------+------------+----------------------+------+------+
   5 rows in set (0.01 sec)

   mysql> SELECT COUNT(*) FROM unistringmapping;
   +----------+
   | COUNT(*) |
   +----------+
   |    19184 |
   +----------+
   1 row in set (0.01 sec)


4. Summarize the status of tables in flute.sql as follows

.. csv-table::
   :header: Table Name, Row Count, Column Names
   :widths: 20, 15, 65
    
   actions_source, 10066005, "``protein1`` | ``protein2`` | ``mode`` | ``sources``"
   biogrid, 344914, "``intID`` | ``entrezA`` | ``entrezB`` | ``bIDA`` | ``bIDB`` | ``nameA`` | ``nameB`` | ``ogsA`` | ``ogsB`` | ``synA`` | ``synB`` | ``expSys`` | ``expSysT`` | ``author`` | ``PubID`` | ``orgA`` | ``orgB`` | ``thput`` | ``scre`` | ``modi`` | ``phen`` | ``qual`` | ``tg`` | ``sourceDB``"
   goterms, 279924, "``b1`` | ``id1`` | ``unknown1`` | ``goterm`` | ``ref`` | ``evidence`` | ``pfam`` | ``unknown2`` | ``name`` | ``lbl`` | ``type`` | ``taxon`` | ``date`` | ``db2``"
   pci_detail, 15473939, "``chem`` | ``prot`` | ``exp`` | ``pred`` | ``data`` | ``text`` | ``score``"
   ppi_actions, 3470907, "``protein1`` | ``protein2`` | ``mode`` | ``action`` | ``direction`` | ``acting`` | ``score``"
   ppi_detail_v11, 11759454, "``protein1`` | ``protein2`` | ``nscore`` | ``fscore`` | ``cscore`` | ``ascore`` | ``escore`` | ``dscore`` | ``tscore``"
   protein_info, 24584629, "``internal_id`` | ``external_id`` | ``species_id`` | ``pref_name``"
   reactome, 61230, "``upID1`` | ``upID2`` | ``intType`` | ``context`` | ``ref``"
   unistringmapping, 19184, "``uniID`` | ``ogs`` | ``stringID`` | ``conf`` | ``unk``"

