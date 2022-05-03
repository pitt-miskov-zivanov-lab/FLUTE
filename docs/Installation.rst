Installation instructions
=========================

MySQL
-----
1. Download the appropriate distribution of `MySQL <https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/>`_.
2. Restart your computer and add to path if necessary.
3. From the command line, access the MySQL environment by typing::

	mysql -u root

If the first prompt fails, you may need to enter the password associated with your computer user account::

	mysql -u root -p

3. You may choose to create a local username and password to keep your database private. 
4. Install `MySQL Python connector <https://dev.mysql.com/doc/connector-python/en/>`_.


FLUTE database
--------------

1. Un-zip the FLUTE.sql file downloaded from BitBucket.
2. Log in to the MySQL environment using your username and password.
3. From there, create an empty database.
4. Log back out, and again from the command line::

	mysql -u username -p database_name < FLUTE.sql

5. If you created a username and password, this will be your username in the above command, but do not enter your password above! Once you hit enter, it will prompt you for the password.
6. You can now run the “run_FLUTE.py” script, you will need to enter the database, host, username, etc. as an argument from the command line.


