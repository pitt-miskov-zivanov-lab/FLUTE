FLUTE usage
===========

1. To filter interactions, run "run_FLUTE.py". You must have Python3 installed.
2. The script takes several parameters:
	A. MySQL username
	B. MySQL password
	C. Host name - “localhost” for MacOSX, desktop name for Windows
	D. Database name (see step 3 from FLUTE DB installation instructions)
	E. Input filename
	F. Output filename for interactions
	G. Output filename for scores
3.	Input files must have the following headers:

	============= =========== ============= ============= =========== ============= =======
	RegulatedName RegulatedID RegulatedType RegulatorName RegulatorID RegulatorType PaperID
	============= =========== ============= ============= =========== ============= =======

4.	Output files include list of reading interactions that pass filtration, and the filtration scores for those filtered interactions.
