import yaml
import os.path
from sys import exit
import sys
import json
import logging
import music_database as mdb
import music_services as ms

# **********************************************************************************
#  Main driving script.
#  It uses music_database.py and music_services.py
#  It will read the configuration in db/music_collection.rc to define
#  api keyfile, artist data filename, and directories to use for logging and output.
#   

# Application name, used when inserting to the database
# Really should move this to the config file....
APP_NAME = "PY_MUSIC_APP"

# Default LOG_LEVEL, this can be set here or in the config file
L_LOG_LEVEL = 'WARNING'

# Default database variables to empty string
DBTYPE = ""
DBUSERNAME = ""
DBPASSWORD = ""

# Local function for messaging, this could also be put into a separate file to be shared
def exit_prog(message):
   message = "Can't find-> " + message
   exit(message)

# Read the config file.  Expects specific file in specific location, didn't see any need to make this configurable
# Cycle through the key/value pairs and define local variables as needed
# yaml expects a file format similar to a Windows .ini file
#  Example
#   FILES:
#          ARTIST_FILE: /tmp/artist.txt
with open(r'db/music_collection.rc') as file:
    opt_list = yaml.full_load(file)

    file_vars = opt_list["FILES"]
    for k in file_vars.split():
        if k.split(":")[0] == "KEYFILE":
           KEYFILE = k.split(":")[1]
           if os.path.exists(KEYFILE):
               print("Exists! Found: ", KEYFILE)
           else:
               exit_prog(KEYFILE)
        if k.split(":")[0] == "ARTIST_FILE":
           ARTIST_FILE = k.split(":")[1]
           if os.path.exists(ARTIST_FILE):
               print("Exists! Found: ", ARTIST_FILE)
           else:
               exit_prog(ARTIST_FILE)

    dir_vars = opt_list["DIRECTORIES"]
    for k in dir_vars.split():
        if k.split(":")[0] == "MC_BASE":
           MC_BASE = k.split(":")[1]
           if os.path.exists(MC_BASE):
               print("Exists! Found: ", MC_BASE)
           else:
               exit_prog(MC_BASE)
        if k.split(":")[0] == "OUTPUT":
           OUTPUT = k.split(":")[1]
           if os.path.exists(OUTPUT):
               print("Exists! Found: ", OUTPUT)
           else:
               exit_prog(OUTPUT)
        if k.split(":")[0] == "LOG":
           LOG = k.split(":")[1]
           if os.path.exists(LOG):
               print("Exists! Found: ", LOG)
           else:
               exit_prog(LOG)
        if k.split(":")[0] == "LOG_LEVEL":
           L_LOG_LEVEL = k.split(":")[1]
           
    db_vars = opt_list["DATABASE"]
    for k in db_vars.split():
        if k.split(":")[0] == "TYPE":
           DBTYPE = k.split(":")[1]
        if k.split(":")[0] == "DBNAME":
           DBNAME = k.split(":")[1]
        if k.split(":")[0] == "USERNAME":
           DBUSERNAME = k.split(":")[1]
        if k.split(":")[0] == "DBPASS":
           DBPASSWORD = k.split(":")[1]
        if k.split(":")[0] == "DBHOST":
           DBHOST = k.split(":")[1]
           

#Prepare logging
logger = logging.getLogger(APP_NAME)
logfilename = LOG + "/" + APP_NAME + ".log"
log_handler = logging.FileHandler(logfilename)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
log_level = logging.getLevelName(L_LOG_LEVEL)
logger.setLevel(log_level)

# Variable to determine if processing should continue, default to False
fcont = False

# Exception file to hold artists that cannot be found
outfile = OUTPUT + "/" + APP_NAME + "_exceptions.txt"
exc_file = open(outfile,"w")

# Artist ID --default to -1 to indicate an invalid artist id
artist_id = -1

# This block attempts to open the key file and read the key.  
# It will read the first line ONLY in the file.  As long as the length of the 
# input string is > 0 it will continue
try:
    fkey = open(KEYFILE,"r")
    apikey = fkey.readline()
    if len(apikey) > 0:
        fcont = True
    else:
        logger.error('No data found')
    fkey.close()
except IOError:
    logger.error('Unable to open file or file not found')
except:    
    logger.error('Other grisly problem opening/reading file')

# Exit if exception thrown or file is empty
if fcont == False:
    logger.error('Quitting')
    exit()

# open the artists file and loop through the data
# Call the service for each artist to get the mbid
fin = open(ARTIST_FILE,"r")
f_readlines = fin.readlines()
 
if DBTYPE != "":
   # Open the database connection
   conn = mdb.connectDb(DBTYPE,DBHOST,DBNAME,DBUSERNAME,DBPASSWORD)
else:
   logger.error('No database defined in configuration file')

# Variable used to log location of program if an error is encountered
statement_id = '0'

# Loop through the records in the artist list
# For each artist found, get the associated albums
# for each alubm, get the associated songs
for x in f_readlines:
    mbid = ms.getArtist(x.strip(),apikey.strip())
    if "Error" in mbid:
        exc_file.write(x.strip() + '\n')
        logger.error('Error, skipping artist, ' +  x.strip())
    else: 
# If an mbid is found for the artist then call the service to get the albums
        logger.info(x.strip())
        albums = ms.getAlbums(x.strip(),apikey.strip())
        if "Error" in albums:
            logger.warning('Error, unable to get albums')
        else:
            artist_id = -1
            for album in albums['topalbums']['album']:
               a_info = ms.getAlbumInfo(x.strip(),album['name'],apikey.strip())
               try:
                   if len(a_info['album']['tracks']['track']) > 0:
                       statement_id = '10'
                       if artist_id == -1:
                            statement_id = '11'
                            artist_id, artist_status, artist_message = mdb.process_artist(DBTYPE,conn,-1,x.strip(),mbid,APP_NAME)                        
                       else:
                            artist_status = 0

                       if artist_status != 0:
                          logger.error('------Artist Return Begin----')
                          logger.error('id: '+ str(artist_id))
                          logger.error('status: '+ str(artist_status))
                          logger.error('message: '+ artist_message)
                          logger.error('artist: ' + x.strip())
                          logger.error('------Artist Return End----')
                       else:
                           statement_id = '15'
                           l_album_name = album['name']
                           album_id, album_status, album_message = mdb.process_album(DBTYPE,conn,-1,artist_id,l_album_name.strip(),APP_NAME)
                           if album_status != 0:
                              logger.error('------Album Return Begin----')
                              logger.error('artist_id: '+ str(artist_id))
                              logger.error('status: '+ str(album_status))
                              logger.error('message: '+ album_message)
                              logger.error('artist: ' + x.strip())
                              logger.error('------Album Return End----')
                           else: 
                               statement_id = '25'
                               for track in a_info['album']['tracks']['track']:
                                   statement_id = '30'
                                   #l_track_name = str(track['name'].encode('utf-8'))
                                   l_track_name = track['name']
                                   statement_id = '31'
                                   track_id, track_status,track_message = mdb.process_track(DBTYPE,conn,-1,artist_id,album_id,l_track_name,APP_NAME)
                                   statement_id = '32'
                                   if track_status != 0:
                                      logger.error('---------Track Error Begin------')
                                      logger.error(' status:' + str(track_status))
                                      logger.error(' message:' + track_message)
                                      logger.error(' artist_id:' + str(artist_id))
                                      logger.error(' album_id:' + str(album_id))
                                      logger.error('---------Track Error End------')

               except:
                     logger.error('EXCEPTION->'+str(sys.exc_info()[0]))
                     logger.error('statement_id:' + statement_id)
                     logger.error('...artist->' + x.strip())
                     logger.error('...artist_id->' + str(artist_id))
                     logger.error('...album_id:' + str(album_id))
                     logger.error('...track:' + l_track_name)

# Close all of the open resources
fin.close()
exc_file.close()
mdb.closeDb(conn)

#for x in f_readlines:
#    similar = ms.getSimilar(x.strip(),apikey.strip())
#    print("artist: ", x.strip())
#    for sim_art in similar['similarartists']['artist']:
#      print("    ",sim_art['name'])
