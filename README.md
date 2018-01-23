------------------------------------------------------------
------------------------------------------------------------
     ______     __  __     __  __     ______   __  __
    /\  ___\   /\ \/ /    /\ \_\ \   /\  == \ /\ \_\ \
    \ \___  \  \ \  _"-.  \ \____ \  \ \  _-/ \ \____ \
     \/\_____\  \ \_\ \_\  \/\_____\  \ \_\    \/\_____\
      \/_____/   \/_/\/_/   \/_____/   \/_/     \/_____/
------------------------------------------------------------
------------------------------------------------------------

Python script that generates and stores object names and other parameters to query simbad and store into a database.

Allows for an easy calling of the data set and read out into sub files

Features:
- Set configuration of location/s
- Initial creation of file list
- Populates filelist parameters from simbad or manual editing allowed
- Add to file list
- automatically determines dates objects are viable
- Allows polling based on object type, seasonal/dates, or regions in the sky
- Allows for output into numerous formats including format for Jskycal
- Robust function allows for declaring of new file type formats and population of said formats


OUTLINE (NEW)
------------------------------------------------------------------------------------------------------------------------

makefile for installation

------------------------------------------------------------------------------------------------------------------------

GUI

> file that allows a gui interface with rest of commands

> allows for loading of config or click gui

------------------------------------------------------------------------------------------------------------------------

CMDRESOLVER

> resolves commands either through config or commandline

------------------------------------------------------------------------------------------------------------------------

QUERY

> ask for command (add location/star(type), query for location/time)

> allows for numerous callings

######################################


>> choose add location

>>> verify source not in SQLSTORAGE

>>> give LOCATIONRESOLVER data or soft warn and search astropy.EarthLocation, hard cancel else)

>>> store data in SQLSTORAGE for location

######################################


>> choose add star

>>> verify source not in sqldatabase based on name

>>> give STARRESOLVER data or soft warn and search astroquery.simbad, hard cancel else

>>> store data in SQLSTORAGE for star

######################################


>> Query location/time

>>> use DATERESOLVER to handle time

>>> verify location in SQLSTORAGE

>>> returns LOCATIONRESOLVER info

>>> pair LOCATIONRESOLVER info with DATERESOLVER info

>>> use above data to calculate what RA DEC is available

>>> poll for all things visible in SQLSTORAGE

>>> return these objects

######################################


>> Query location/star

>>> verify location in SQLSTORAGE

>>> returns LOCATIONRESOLVER info

>>> verify star/type in SQLSTORAGE

>>> return STARRESOLVER info

>>> pair LOCATIONRESOLVER info with STARRESOLVER info

>>> use above to calculate when RA DEC is visible

>>> return these times

------------------------------------------------------------------------------------------------------------------------

LOCATIONRESOLVER

> resolves the location to a standard form

> use lat, long, name, tz, T/F for DST

> can resolve using astropy.EarthLocation

------------------------------------------------------------------------------------------------------------------------

STARRESOLVER

> input right info (name1,name2 type, ra,dec,epoch,ubvrigjhk,lastupdate)

------------------------------------------------------------------------------------------------------------------------

DATERESOLVER

> resolves the date to a standard form

> use datetime

------------------------------------------------------------------------------------------------------------------------

SQLSTORAGE

> location database and star database

> store/serve the sql database

> read lines from sql database

> write new lines to the database

------------------------------------------------------------------------------------------------------------------------

Save Structure

> Skypy

>> runskypywithgui.py, runskypywithoutgui.py

>> skypy/*source

>> database

>>> location.sql, star.sql

------------------------------------------------------------------------------------------------------------------------

WorkFlow



------------------------------------------------------------------------------------------------------------------------
