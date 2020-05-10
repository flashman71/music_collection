import requests
import json
import os
import sys

# ******************************************************************
#   Functions for accessing lsat.fm web services
#
#   Requires:
#            last.fm api key --must sign up on last.fm website
#
# ******************************************************************

# Retrieves the band/musician from the last.fm database
#  Input(s):
#           artist name
#           api key
#  Return(s):
#            Artist MBID or failure message
def getArtist(artist_name,api_key):
    try:
        payload = {
            'api_key': api_key,
            'method': 'artist.getinfo',
            'format': 'json',
            'artist': artist_name
        }

        headers = {
            'user-agent': 'PrivateApp'
        }

        r = requests.get('http://ws.audioscrobbler.com/2.0/',headers=headers,params=payload)
        if r.status_code != 200:
            print("Fucked up")
            return "Fucked Up"

        resp_json = r.json()
        return resp_json['artist']['mbid']
    except KeyError:
        return "Error, unable to find band"


# Retrieves the albums belonging to the band/musician from the last.fm database
#  Input(s):
#           artist name
#           api key
#  Return(s):
#            JSON document of albums --see ws.audioscrobbler.com for layout
#              or failure message
def getAlbums(artist_name,api_key):
    try:
        payload = {
            'api_key': api_key,
            'method': 'artist.gettopalbums',
            'format': 'json',
            'artist': artist_name
        }

        headers = {
            'user-agent': 'PrivateApp'
        }

        r = requests.get('http://ws.audioscrobbler.com/2.0/',headers=headers,params=payload)
        if r.status_code != 200:
            print("Fucked up")
            return "Fucked Up"

        return r.json()
    except KeyError:
        return "Error, unable to find albums"

# Retrieves the tracks for an album belonging to the band/musician from the last.fm database
#  Input(s):
#           artist name
#           album name
#           api key
#  Return(s):
#            JSON document of tracks --see ws.audioscrobbler.com for layout
#              or failure message
def getAlbumInfo(artist_name,album_name,api_key):
    try:
        payload = {
            'api_key': api_key,
            'method': 'album.getInfo',
            'format': 'json',
            'artist': artist_name,
            'album':  album_name
        }

        headers = {
            'user-agent': 'PrivateApp'
        }

        r = requests.get('http://ws.audioscrobbler.com/2.0/',headers=headers,params=payload)
        if r.status_code != 200:
            print("Fucked up")
            return "Fucked Up"

        return r.json()
    except KeyError:
        return "Error, unable to find albums"

# Retrieves similar artists
#  Input(s):
#           artist name
#           api key
#  Return(s):
#            JSON document of similar artists --see ws.audioscrobbler.com for layout
#              or failure message
def getSimilar(artist_name,api_key):
    try:
        payload = {
            'api_key': api_key,
            'method': 'artist.getsimilar',
            'format': 'json',
            'artist': artist_name
        }

        headers = {
            'user-agent': 'PrivateApp'
        }

        r = requests.get('http://ws.audioscrobbler.com/2.0/',headers=headers,params=payload)
        if r.status_code != 200:
            print("Fucked up")
            return "Fucked Up"

        return r.json()
    except KeyError:
        return "Error, unable to find similar artists"
