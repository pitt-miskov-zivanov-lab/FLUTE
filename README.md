# FLUTE

This is the documentation for the FLUTE tool and associated database. 

To run FLUTE (interaction filtering) involves two files:

-MySQL data dump containing all tables

-Python 3.6 script "run_flute.py" for filtering interactions


1. Download .SQL file and import into local MySQL database
2. Run script, with the username, password, host, and database name of your local database.
3. Input file shpuld contain the following headers : 'RegulatedName','RegulatedID','RegulatedType','RegulatorName','RegulatorID','RegulatorType','PaperID'
4. Duplicated may be added with the '-g' option

Additional filtering functionality:

Filtering interactions by year, retrieving related papers, or adding related interactions require the additional files:

-Python 3.6 script "years.py" for creating NumPy array with data on all PMCIDs
-Plain text file containing data on all PMCIDs