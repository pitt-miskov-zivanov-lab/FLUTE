# FLUTE

This is the documentation for the FLUTE tool and associated database. This repository contains three files -

-MySQL data dump containing all tables

-Python 3.6 script  

-NumPy array with data on all papers from PMCID

To run FLUTE:

1. Download .SQL file and import into local MySQL database
2. Run script, with the username, password, host, and database name of your local database.
3. Input file shpuld contain the following headers : 'RegulatedName','RegulatedID','RegulatedType','RegulatorName','RegulatorID','RegulatorType','PaperID'
