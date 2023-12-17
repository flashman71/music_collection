import requests
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Spotify authorization token
def spotify_auth(client_id,client_secret,redirect_url,scope):
   return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url,scope=scope))


# Spotify track ids
def get_track_ids(sp,time_frame):
   track_ids = []
   for song in time_frame['items']:
       track_ids.append(song['id'])
   return track_ids

# Spotify track data
def get_track_features(sp,id):
   meta = sp.track(id)
 # meta
   name = meta['name']
   album = meta['album']['name']
   artist = meta['album']['artists'][0]['name']
   spotify_url = meta['external_urls']['spotify']
   album_cover = meta['album']['images'][0]['url']
   track_info = [name, album, artist, spotify_url, album_cover]
   return track_info

# Create csv file of retrieved Spotify data
def convert_to_df(sp,track_ids,time_period):
 # loop over track ids
   tracks = []
   for i in range(len(track_ids)):
     track = get_track_features(sp,track_ids[i])
     tracks.append(track)
 # create dataset
     df = pd.DataFrame(tracks, columns = ['Track', 'Album', 'Artist', 'Spotify Link', 'Album Cover'])
 # save to CSV
     filename = f'sp_data_{time_period}.csv'
     df.to_csv(filename)
   return filename
