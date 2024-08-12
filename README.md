# Add required data to AAVSO VPHOT upload using Slooh FITS files
****************************************************************
app.py adds additionally required data to the header of Slooh FITS file(s) for a successful VPHOT upload on AAVSO site.

Python 3 code is to add following data to the header of the selected FIT file(s):
- the name of the object
- Ra and Dec coordinates
- the filter used in the observation
- the air mass of the object at the time of the observation. 
 
This data addition simplifies the upload process for AAVSO upload.

Required files:
================
1. app.py program 
2. FITS files from Slooh 

IMPORTANT Ra and Dec coordinates and the observation date & time has to be in the file name. The date & time are there always, but instead of the coordinate, often the object is inserted to the name. But a good thing is that for for variable stars this is usually not the case. In that case the name of the object has to be replaced with the coordinates.

Running the program:
====================
FITS file will be rewritten, so in case you need the originals, save them before using the app.

Start add.py with your python platform
- program requests to choose the FITS file(s) from your computer. You can choose one or more files for the <ul>same</ul> object.
- after the file selection, the program asks for the name of the object.
- the files are updated (rewritten) and no new files are created.

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
Ver 1 30.6.2021 (asSFAu.py)
Ver 2 12.8.2024

Credits:
========
Air mass calculations based on functions based on Paul Schlyter's web site https://stjarnhimlen.se/comp/ppcomp.html
