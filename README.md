# VIOLIN
[![Documentation Status](https://readthedocs.org/projects/flute/badge/?version=latest)](https://flute.readthedocs.io/en/latest/?badge=latest)

Purpose: Understanding disease at the cellular level requires detailed knowledge of signaling networks. To aid in this task, many advances have been made in the field of natural language processing (NLP) to extract signaling events from biomedical literature. However, even state-of-the-art NLP methods incorrectly interpret some signaling events described in the literature. The FiLter for Understanding True Events (FLUTE) tool seeks to identify high-confidence signaling events from biomedical NLP output by comparing with existing biological databases. As such, FLUTE can reliably determine the confidence in the biomolecular events extracted by NLP methods and at the same time provide a speedup in event filtering by three orders of magnitude. <br>

<br>
FLUTE DB installation instructions:<br>
    -Un-zip the FLUTE.sql file downloaded from BitBucket.<br>
    -Log in to the MySQL environment using your username and password. <br>
    -From there, create an empty database (any name is fine, I recommend the classic “FLUTE”). <br>
    -Log back out, and again from the command line <br>
        > mysql -u username -p database_name < FLUTE.sql <br>
    -If you created a username and password, this will be your username in the above command, but do not enter your password above! Once you hit enter, it will prompt you for the password. <br>
    -You can now run the “run_FLUTE.py” script, you will need to enter the database, host, username, etc. as an argument from the command line. <br>

<br>
FLUTE usage:<br>
    To filter interactions, run "run_FLUTE.py". You must have Python3 installed. <br>
    The script takes several parameters:
        MySQL username
        MySQL password
        Host name - “localhost” for MacOSX, desktop name for Windows
        Database name (see step 3 from FLUTE DB installation instructions)
        Input filename
        Output filename for interactions
        Output filename for scores

Input files must have the following headers:
    RegulatedName, RegulatedID, RegulatedType, RegulatorName, RegulatorID, RegulatorType, PaperID

Output files include list of reading interactions that pass filtration, and the filtration scores for those filtered interactions.

MySQL installation instructions and troubleshooting:
    1.	Download the appropriate distribution for your OS from (https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)
    2.	Restart your computer, and add to path if necessary.
    3.	From the command line, access the MySQL environment by typing:
        >mysql -u root
        If the first prompt fails, you may need to enter the password associated with your computer user account:
        >mysql -u root -p
    4.  You may choose to create a local username and password to keep your database private. However, this is published information, so it is not a security risk if you do not have a password.
    5.  Install MySQL Python connector (https://dev.mysql.com/doc/connector-python/en/)
