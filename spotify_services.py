import requests 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

API_URL = "https://api.spotify.com/v1"

def get_sp_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    })
    auth_data = auth_response.json()
    access_token = auth_data.get("access_token")
    return access_token

def search_album(sp,artist_name,album_name):
    headers = {
        "Authorization": f"Bearer {sp}"
    }
    params = {
        "q": f"artist:{artist_name} album:{album_name}",
        "type": "album",
        "limit": 5
    }
    response = requests.get(f"{API_URL}/search",headers=headers,params=params)
    response_data = response.json()

    print("DEBUG:",response_data)
    album_info = {}
    if "albums" in response_data and "items" in response_data["albums"]:
        album_items = response_data["albums"]["items"]
        for album in album_items:
             if album.get("name").lower() == album_name.lower(): #and album.get("release_date") == "1982":
                 print("DEBUG->Album Name: ", album.get("name"))
                 print(".....->Release Date: ",album.get("release_date"))
                 print(".....->Num Tracks: ", album.get("total_tracks"))
            #print("DEBUG->Artist Name: ", for artist in album.get("artists",[]))

    return album_info
            
def search_artist(sp,artist_name):
    # Perform the artist search
    headers = {
        "Authorization": f"Bearer {sp}"
    }
    params = {
        "q": f"artist:{artist_name}",
        "type": "artist",
        "limit": 5
    }
    response = requests.get(f"{API_URL}/search",headers=headers,params=params)
    response_data = response.json()
    print("DEBUG:",response_data)
#    results = sp.search(q=artist_name, type='artist', limit=1)

    # Extract and return the artist information
#    if results['artists']['items']:
#        artist = results['artists']['items'][0]
#        print("DEBUG->ARTIST:",artist)
#        return artist
#    else:
#        return None

def get_album(sp, artist_id,album_name):
    results = sp.artist_albums(artist_id,album_type='album',limit=50)

    print("DEBUG>Searching for: ",album_name.lower())
    print("DEBUG->Results: ", results)
    for album in results['items']:
        print("DEBUG->Album(o):",album['name'].lower())
        if album['name'].lower() == album_name.lower():
            tracks = sp.album_tracks(album['id'])
            #for t in tracks['items']:
                #print("DEBUG:TRACK INFO:", t['name'],t['duration_ms'],t['track_number'])
            # Calculate the total duration of the album
            total_duration_ms = sum([track['duration_ms'] for track in tracks['items']])
            total_duration_seconds = total_duration_ms / 1000
        #print(".... total duration minutes:",f'{(total_duration_seconds/60):.2f}')
            print("DEBUG->Album name:",album['name'])
            print("DEBUG->.....len:", f'{(total_duration_seconds/60):.2f}')
        #    upd_stmt = "update mus_owner.album set duration_min = " + f'{(total_duration_seconds/60):.2f}' + " where full_album_name = '" + album_name.strip().replace("'","''") + "';"
        #print("update mus_owner.album ma set duration_mins = ",f'{(total_duration_seconds/60):.2f}')
    #    print(upd_stmt)
           # return total_duration_seconds
#            print("DEBUG->ALBUM:",album)
        return album

    return None

def get_top_tracks(sp):
    print("DEBUG->get_top_tracks")
    access_token = sp['access_token']
    sobj = spotipy.Spotify(auth=access_token)
    results = sp.current_user_top_tracks(limit=20, time_range='medium') 
    print(results)
    print("DEBUG->end get_top_tracks")
    return results
