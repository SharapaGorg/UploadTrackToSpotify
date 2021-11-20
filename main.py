import spotipy
from spotipy.oauth2 import SpotifyOAuth
from utils import upload_tracks_from_vk
import json
import requests

#https://developer.spotify.com/dashboard/applications/ - create app and copy client_id and client_secret

CACHE = dict()
BASE_PLAYLIST = 'FONK!!!FONK!!!FONK'
TRACKS_TITLES = upload_tracks_from_vk('https://vk.com/music/playlist/170735510_38_018f4a24a2643650f3')
TRACKS = list()

scope = "playlist-modify-public"
client_id = '757f54acd64b49949e2350dea57815c6'
client_secret = '54f60852f05847368e2133f2b7d1eb0a'
redirect_uri = 'http://127.0.0.1:5000/spotipy/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, 
                                               client_id=client_id, 
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri))

with open('.cache', 'r') as read_stream:
    content = read_stream.read()
    CACHE = json.loads(content)

for track in TRACKS_TITLES:
    result = sp.search(q = 'track:' + track, type = 'track')
    
    try:
        _ = result['tracks']['items']
            
        for elem in _:
            print(elem.get('name').lower(), track.lower())
            if elem.get('name').replace(' ', '').lower() == track.replace(' ', '').lower():
                TRACKS.append(elem.get('id'))
                print(f'Successfuly added {track} [+]')
                break
            else:
                print(f'Spotify has not track named {track} [-]')
    except:
        print(f'Spotify has not track named {track} [-]')

playlists = sp.current_user_playlists().get('items')

for playlist in playlists:
    if playlist.get('name') == BASE_PLAYLIST:
        tracks_in_this_playlist = list()
        for elem in json.loads(requests.get(playlist['tracks']['href'] + '?access_token=' + CACHE.get('access_token')).text)['items']:
            tracks_in_this_playlist.append(elem['track'].get('id'))
            
        sp.playlist_add_items(playlist.get('id'), TRACKS, position=0)
        # sp.playlist_remove_all_occurrences_of_items(playlist.get('id'), tracks_in_this_playlist)