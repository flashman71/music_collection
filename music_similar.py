import yaml
import os.path
from sys import exit
import sys
import json
import logging
import music_database as mdb
import music_services as ms
from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://galileo:7687", auth=("neo4j", "neo5j"),encrypted=False)

def add_artist(tx, name, artist_name):
    tx.run("MERGE (a:Artist {name: $name}) "
           "MERGE (a)-[:SIMILAR_TO]->(artist:Artist {name: $artist_name})",
           name=name, artist_name=artist_name)

def print_artists(tx, name):
    for record in tx.run("MATCH (a:Artist)-[:KNOWS]->(artist) WHERE a.name = $name "
                         "RETURN artist.name ORDER BY artist.name", name=name):
        print(record["artist.name"])



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

def exit_prog(message):
   message = "Can't fucking find-> " + message
   exit(message)

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

    for k in file_vars.split():
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
               exit_prog(MC_BASE)
        if k.split(":")[0] == "LOG_LEVEL":
           L_LOG_LEVEL = k.split(":")[1]
           

#Prepare logging
logger = logging.getLogger(APP_NAME)
logfilename = LOG + "/" + APP_NAME + ".log"
log_handler = logging.FileHandler(logfilename)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
log_level = logging.getLevelName(L_LOG_LEVEL)
logger.setLevel(log_level)

# File to hold artists that cannot be found
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


# open the artists file and loop through the data
# Call the service for each artist to get the mbid
fin = open(ARTIST_FILE,"r")
f_readlines = fin.readlines()
 
# Variable used to log location of program if an error is encountered
statement_id = '0'

# Loop through the records in the artist list
for x in f_readlines:
    mbid = ms.getArtist(x.strip(),apikey.strip())
    if "Error" in mbid:
        exc_file.write(x.strip() + '\n')
        logger.error('Error, skipping artist, ' +  x.strip())
    else: 
        similar = ms.getSimilar(x.strip(),apikey.strip())
        print("artist: ", x.strip())
        for sim_art in similar['similarartists']['artist']:
           #print(x.strip(),':',sim_art['name'])
           with driver.session() as session:
               session.write_transaction(add_artist, x.strip(), sim_art['name'])

fin.close()
driver.close()
