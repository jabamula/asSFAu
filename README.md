# asSFAu
***********************************************
asSFAu.py  add some data to the header of Slooh FITS file(s) for AAVSO VPHOT upload

Program code is Python 3.7 to add following data to the header of the selected FIT file(s):
- the name of the object
- Ra and Dec coordinates
- the air mass of the object at the time of the observation. 
 
This data addition simplifies the upload process for AAVSO upload.

Required files:
================
1. asSFAu.py program 
2. FITS files from Slooh 

IMPORTANT Ra and Dec coordinates and the observation date & time has to be in the file name. The date & time are there always, but instead of the coordinate, often the object is inserted to the name. But a good thing is that for for variable stars this is usually not the case. In that case the name of the object has to be replaced with the coordinates.

Running the program:
====================
Start asSFAu.py with your python platform
- choose the FITS file(s) from your computer. You can choose one or more files for the same object.
- after the file selection, the program will ask for the name of the object.
- the files are updated and no new files are created.

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

Example:
========
Attached is Example.jpg showing what lines is added to the FITS file header

Version history:
================
Ver 1.0 30.6.2021
- first version, 

Credits:
========
Air mass calculations based on functions based on Paul Schlyter's web site https://stjarnhimlen.se/comp/ppcomp.html
