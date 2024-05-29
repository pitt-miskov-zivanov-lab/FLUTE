# FLUTE
[![Documentation Status](https://readthedocs.org/projects/melody-flute/badge/?version=latest)](https://melody-flute.readthedocs.io/en/latest/?badge=latest)

### (The FiLter for Understanding True Events)

The FiLter for Understanding True Events (FLUTE) tool seeks to identify high-confidence signaling events from biomedical NLP output by comparing with existing biological databases. As such, FLUTE can reliably determine the confidence in the biomolecular events extracted by NLP methods and at the same time provide a speedup in event filtering by three orders of magnitude.

## Contents

- [Purpose](#Purpose)
- [Installation](#Installation)
- [Usage](#Usage)
- [MySQL](#MySQL)
- [Citation](#Citation)
- [Funding](#Funding)
- [Support](#Support)

## Purpose
Understanding disease at the cellular level requires detailed knowledge of signaling networks. To aid in this task, many advances have been made in the field of natural language processing (NLP) to extract signaling events from biomedical literature. However, even state-of-the-art NLP methods incorrectly interpret some signaling events described in the literature.

## Installation
- Unzip the [`flute.sql.zip`](supplementary/flute.sql.zip) file.
- Log in to the MySQL environment using your username and password.
- From there, create an empty database named ``YOUR_DATABASE_NAME``(any name is fine, I recommend the classic ``flute``).
- Log back out, and again from the command line
  ```
  mysql -u YOUR_USER_NAME -p YOUR_DATABASE_NAME < flute.sql
  ```
- If you created a username and password, this will be your username in the above command, but do not enter your password above! Once you hit enter, it will prompt you for the password.
- You can now run the [`run_FLUTE.py`](src/run_FLUTE.py) script, you will need to enter the database, host, username, etc. as an argument from the command line.

## Usage
To filter interactions, run [`run_FLUTE.py`](src/run_FLUTE.py). You must have Python3 installed. The script takes several parameters:
- MySQL username
- MySQL password
- Host name - ``localhost`` for macOS/Linux, desktop name for Windows
- Database name (``YOUR_DATABASE_NAME``)
- Input filename
- Output filename for interactions
- Output filename for scores

Input files must have the following headers: ``RegulatedName, RegulatedID, RegulatedType, RegulatorName, RegulatorID, RegulatorType, PaperID``. Output files include list of reading interactions that pass filtration, and the filtration scores for those filtered interactions.

For additional FLUTE functionality beyond interaction filtering (get related papers, related interactions in databases, etc.), check python -h

## MySQL
- Download the appropriate distribution for your OS from [here](https://dev.mysql.com/downloads/mysql/)
- Restart your computer, and add to path if necessary.
- From the command line, access the MySQL environment by typing:
  ```
  mysql -u root
  ```
  If the first prompt fails, you may need to enter the password associated with your computer user account:
  ```
  mysql -u root -p
  ```
- You may choose to create a local username and password to keep your database private. However, this is published information, so it is not a security risk if you do not have a password.
- Install [MySQL Python connector](https://dev.mysql.com/doc/connector-python/en/)

## Citation

_Emilee Holtzapple, Cheryl A Telmer, Natasa Miskov-Zivanov, FLUTE: Fast and reliable knowledge retrieval from biomedical literature, Database, Volume 2020, 2020, https://doi.org/10.1093/database/baaa056_

## Funding

This work was funded in part by DARPA Big Mechanism award, AIMCancer (W911NF-17-1-0135); and in part by the University of Pittsburgh, Swanson School of Engineering.

## Support
_To be updated_
