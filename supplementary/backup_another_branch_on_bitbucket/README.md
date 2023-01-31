Python version: 3.6

The FLUTE database is stored as a zipped .sql file. To run fLUTE, you must first download and import the .sql into your local MySQL database. 

To filter interactions, run "run_FLUTE.py". Input files must have the following headers:

    RegulatedName,RegulatedID,RegulatedType,RegulatorName,RegulatorID,RegulatorType,PaperID

For additional FLUTE functionality beyond interaction filtering (get related papers, related interactions in databases, etc.), 
first run "years.py".
