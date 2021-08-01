# asSFAu
***********************************************
asSFAu.py  add some data to Slooh FITS files to AAVSO VPHOT upload

Program made in Python 3.7 to add the name of the object, Ra and Dec as well as the air mass. Simplifies the upload process for AAVSO upload.

Required files:
================
1. asSFAu.py program 
2. FITS files from Slooh with Ra and Dec coordinates in the file name

Running the program:
====================
Start NSO.py with your python platform
- choose the FITS file(s) from your computer. You can choose one or more files for the same object.
- after the file selection, the program will ask for the name of the project
- the files are updated

Python modules:
===============
The Python modules are all usually within Python 3.7 environment, but might needed to be installed. 
- panda
- matplotlib
- math
- datetime
- re
- csv
- pathlib
- Tk
- astropy.io

Version history:
================
Ver 1.0 30.6.2021
- first version

Credits:
========
Air mass calculations based on functions based on Paul Schlyter's web site https://stjarnhimlen.se/comp/ppcomp.html
