Installation instructions
=========================

MySQL
-----
1. Download the appropriate distribution of `MySQL <https://dev.mysql.com/downloads/mysql/>`_. During the installation process, you will be asked to create a local username (``root`` will be default username) and password to keep your database private.

.. Attention::
 Test your installation via typing ``mysql`` in terminal. If it's not a recognized command, you may need to permanently add it to environmental path and restart your computer.

2. From the command line, access MySQL environment by typing::

	mysql -u root

   or replacing ``root`` with your customized username::
   
   	mysql -u YOUR_USER_NAME

   You can exit MySQL environment by typing ``\q``.

.. Attention::
 If the prompt fails, you may need to enter the password associated with your user account (set in step 1 during installation)::

	mysql -u root -p
 
 or::
 
 	mysql -u YOUR_USER_NAME -p
 
3. Install `MySQL Python connector <https://dev.mysql.com/doc/connector-python/en/>`_. If **pip** has been installed on your computer, use::

	pip install mysql-connector-python


FLUTE database
--------------

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

4. You can now run FLUTE tool (via terminal, Jupyter notebook or GUI), you will need to enter the database name (``YOUR_DATABASE_NAME``), host name (``localhost`` for MacOS/Linux and desktop name for Windows), MySQL username (``root`` or ``YOUR_USER_NAME``) and MySQL password as arguments.
 for Windows), username, etc. as an argument from the command line.
