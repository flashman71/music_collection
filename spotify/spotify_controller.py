import argparse
import logging
import os
import sys
import spotipy_services as ss
import spotify_utility_services as sus

#$HOME/.music_collection/sp_keyfile

APP_NAME="spotify_controller"
L_LOG_LEVEL='WARNING'
LOG="/var/log/local/spotify"

# Default home directory and filename, can be overridden with -f/--file switch
#home_directory = os.path.expanduser("~")
base_directory = "/usr/local/etc"
filename = ".music_collection/sp_config"

# Combine the home directory, filename, and extension
SP_KEYFILE = os.path.join(base_directory, filename)

# Collect any command line arguments
parser = argparse.ArgumentParser(description='A script with command line switches.')

    # Define command line switches
parser.add_argument('-f', '--file', dest='file_path', help='Path to the Spotify input file')

# Check for a comman line argument, this would override the default file containing the Spotify credentials
if len(sys.argv) > 1:
    # Parse command line arguments
    args = parser.parse_args()
    # Access the values of the switches
    SP_KEYFILE = args.file_path
    if not os.path.exists(SP_KEYFILE):
         exit("File not found....",SP_KEYFILE)        

#Prepare logging
logger = logging.getLogger(APP_NAME)
logfilename = LOG + "/" + APP_NAME + ".log"
log_handler = logging.FileHandler(logfilename)
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
log_level = logging.getLevelName(L_LOG_LEVEL)
logger.setLevel(log_level)

# Open the configuration file and parse, must be separated by "="
fkey = open(SP_KEYFILE,"r")
for line in fkey:
    line = line.strip()
    if line:
        key,value = line.split('=',1)
        if key == "CLIENT_ID":
            SPOTIFY_CLIENT_ID = value.strip()
        if key == "CLIENT_SECRET":
            SPOTIFY_CLIENT_SECRET = value.strip()
        if key == "SPOTIPY_REDIRECT_URI":
            SPOTIPY_REDIRECT_URI = value.strip()
        if key == "SCOPE":
            SCOPE = value.strip()
        if key == "REM_SERVER":
            REM_SERVER = value.strip()
        if key == "REM_PORT":
            REM_PORT = int(value.strip())
        if key == "REM_USER":
            REM_USER = value.strip()
        if key == "REM_PASS":
            REM_PASS = value.strip()

if len(SPOTIFY_CLIENT_ID) > 0 and len(SPOTIFY_CLIENT_SECRET) > 0:
    fcont = True
else:
    logger.error('No data found')
fkey.close()

# Get the Spotify token
sp = ss.spotify_auth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE)

# Get the top tracks for the available Spotify time ranges
time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    tracks = sp.current_user_top_tracks(limit=25, offset=0, time_range=time_period)
    track_ids = ss.get_track_ids(sp,tracks)
    ret_filename = ss.convert_to_df(sp,track_ids,time_period)
# Convert to html
    html_file = sus.output_to_html(ret_filename)


# Upload if remote server, user, and password are defined
if REM_SERVER is not None and REM_USER is not None and REM_PASS is not None:
#     sus.sftp_upload(REM_SERVER,REM_PORT,REM_USER,REM_PASS,html_file,"")
     sus.sftp_upload_mult(REM_SERVER,REM_PORT,REM_USER,REM_PASS,"sp_data*.html","")
