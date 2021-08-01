import math
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
from pathlib import Path
from tkinter import Tk     # from tkinter import Tk for Python 3.x
#from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from astropy.io import fits
#from astropy.utils.data import get_pkg_data_filename

# Ver 1.0 30.6.2021 by Jari Backman
# Program made in Python 3.7 to add the name of the object, Ra and Dec as well as the air mass.
# Simplifies the upload process for AAVSO upload.
# Air mass calculations based on functions based on Paul Schlyter's web site https://stjarnhimlen.se/comp/ppcomp.html

# constants
pi = 3.14159265359;
radeg = 180/pi;
fii = 90;

# arcsin and arccos
def fnasin(x):
    return math.atan(float(x)/math.sqrt(1-float(x)*float(x)));

def fnacos(x): 
    return (pi/2 - fnasin(float(x)));

# Trig. functions in degrees
def fnsind(x):
    return math.sin(float(x)/radeg);

def fncosd(x):
    return math.cos(float(x)/radeg);

def fntand(x):
    return math.tan(float(x)/radeg);

def fnasind(x):
    if x == 1:
        return pi / 2;
    elif x == -1:
        return - pi/2;
    else:
        return radeg*math.atan(float(x)/math.sqrt(1-float(x)*float(x)));

def fnacosd(x):
    return 90 - fnasind(float(x));

def fnatand(x):
    return radeg*math.atan(float(x));
#
# arctan in all four quadrants
def fnatan2(y,x):
    if x == 0.0:
        if y == 0.0:
            return 99.9;
        elif y > 0.0:
            return pi / 2;
        else:
            return - pi / 2;
    else:
        if x > 0.0:
            return math.atan(float(y/x));
        elif x < 0.0:
            if y >= 0.0:
                return math.atan(float(y/x)) + pi;
            else:
                return math.atan(float(y/x)) - pi;

def fnatan2d(y,x):
    return radeg*fnatan2((y/radeg),(x/radeg));

# Normalize an angle between 0 and 360 degrees
# Use Double Precision, if possible
def fnrev(x):
    rv = x - math.trunc(float(x/360.0))*360.0;
    if rv < 0.0:
        return rv + 360;
    return rv;

# Cube Root (needed for parabolic orbits)
def fncbrt(x):
    if x > 0:
        return math.exp( math.log(x)/3 );
    elif x < 0:
        return - math.exp( math.log(-x)/3 );
    else:
        return 0;

# spherical to rectangular coordinates
def sphe2rect(r,RA,Decl):
    x = r * fncosd(RA) * fncosd(Decl); 
    y = r * fnsind(RA) * fncosd(Decl);
    z = r * fnsind(Decl);
    return x,y,z;

# rectangular to spherical coordinates
def rect2sphe(x,y,z):
    r    = math.sqrt( x*x + y*y + z*z );
    RA   = fnatan2d( y, x );
    Decl = fnatan2d( z, math.sqrt( x*x + y*y ) );
    return r,RA,Decl;

# ecliptic to equatorial coordinates
def eclip2equat(x,y,z,o):
    xequat = x;
    yequat = y * fncosd(o) - z * fnsind(o);
    zequat = y * fnsind(o) + z * fncosd(o);
    return xequat, yequat, zequat;

# equatorial to ecliptic coordinates
def equat2eclip(x,y,z,o):
    xeclip = x;
    yeclip = y * fncosd(o) + z * fnsind(o);
    zeclip = -y * fnsind(o) + z * fncosd(o);
    return xeclip, yeclip, zeclip;

# function for converting degrees, minutes, seconds (DMS) coordinates to decimal degrees (DD)
def dms_to_dd(d, m, s):
    dd = float(d) + float(m)/60 + float(s)/3600;
    return dd

# function for converting decimal degrees (DD) to degrees, minutes, seconds (DMS) coordinates
def dd_to_dms(dd):
    mnt,sec = divmod(dd*3600,60)
    deg,mnt = divmod(mnt,60)
    deg = int(deg);
    mnt = int(mnt);
    return deg,mnt,sec;


def cobj(Y, M, D, UT, Ra, Decl, LON, lat):
    # date calculation
    d = 367*Y - (7*(Y + ((M+9)//12)))//4 + (275*M)//9 + D - 730530;

    # obliquity of the ecliptic
    oblecl = 23.4393 - 3.563E-7 * d;

    # Sidereal Time for the time meridian of Central Europe at UTC 0.00 (noe lon = 15°)
    # first in degrees, fit 0 to 360 and lastly divide with 15 to hours
    
    SIDTIME = fnrev((100.4606184 + 0.9856473662862 * d + UT*15 + LON) / 15);
    #
    if SIDTIME > 24:
        SIDTIME = SIDTIME - 24;
    elif SIDTIME < 0:
        SIDTIME = SIDTIME + 24;

    #The Hour Angle in hours
    HA = SIDTIME - RA;
    #The Hour Angle in hours
    HA = HA * 15;

    # Convert Sun's HA and Decl to a rectangular (x,y,z) coordinate system 
    x = fncosd(HA) * fncosd(Decl);
    y = fnsind(HA) * fncosd(Decl);
    z = fnsind(Decl);

    # Rotate this x,y,z system along an axis going east-west, L is +15deg, lat +60deg
    # ask latitude
    xhor = x * fnsind(lat) - z * fncosd(lat);
    yhor = y;
    zhor = x * fncosd(lat) + z * fnsind(lat);

    #azimuth, altitude
    azimuth  = fnatan2d( yhor, xhor ) + 180;
    altitude = fnatan2d( zhor, math.sqrt(xhor*xhor+yhor*yhor) );
    return azimuth, altitude;

# datetime object containing current date and time
today = datetime.now()

# we don't want a full GUI, so keep the root window from appearing
Tk().withdraw()

# show an "Open" dialog box and return the path to the selected file
starfiles = askopenfilenames(title = "Open FIT file(s)")

# get the name of the object
object = input("Name of the object: ")

# go through each object
for starfile in starfiles:

    #only the file name from full path
    sloohfile = Path(starfile).stem
    
    # extract different parts of the file name
    ra = sloohfile[0:6]
    decmark = sloohfile[6:7]
    dec = sloohfile[7:13]
    stardate = sloohfile[14:22]
    startime = sloohfile[23:29]

    # extract date and time details
    Y = int(stardate[0:4]);
    M = int(stardate[4:6]);
    D = int(stardate[6:]);
    H = int(startime[0:2]);
    Mi = int(startime[2:4]);
    S = int(startime[4:]);

    # accurate hour of the observation
    UT = H + Mi / 60 + S / 3600

    # read the observatory
    hdul = fits.open(starfile)
    observer = hdul[0].header['OBSERVER']
    if "Canary" in observer:
        LON = -16.50826;
        LAT = 28.2997;
    else:
        LON = -70.534;
        LAT = -33.269;

    # decimal ra and dec values
    RA = dms_to_dd(int(ra[0:2]),int(ra[2:4]),int(ra[4:]));
    Decl = dms_to_dd(int(dec[0:2]),int(dec[2:4]),int(dec[4:]));
    
    # declination front sign
    if decmark == 'm':
        Decl = -1.0 * Decl;
    
    # calculating the azimuth and altitude of the object
    azimuth, altitude = cobj(Y, M, D, UT, RA, Decl, LON, LAT);

    # calculating the airmass
    zen = 90 - altitude
    pi = 3.14159265359
    zen = zen * pi / 180
    am = 1 / math.cos (zen)

    # adding to the FITS file missing information
    fits.setval(starfile, 'OBJECT', value=object)
    fits.setval(starfile, 'RA', value=RA)
    fits.setval(starfile, 'DEC', value=Decl)
    fits.setval(starfile, 'AIRMASS', value=am)
    fits.setval(starfile, 'HISTORY', value=' Missing values Object, Ra, Dec and airmass added JB/Slooh')
