from spotipy.oauth2 import SpotifyOAuth
from utils import Uploader

#https://developer.spotify.com/dashboard/applications/ - create app and copy client_id and client_secret

CACHE = dict()
BASE_PLAYLIST = 'FONK!!!FONK!!!FONK'
TRACKS = list()

client_id = '757f54acd64b49949e2350dea57815c6'
client_secret = '54f60852f05847368e2133f2b7d1eb0a'
redirect_uri = 'http://127.0.0.1:5000/spotipy/'

uploader = Uploader(client_id, client_secret, redirect_uri, debug_mode=False)
uploader.upload_tracks_from_vk('https://vk.com/music/playlist/170735510_38_018f4a24a2643650f3', BASE_PLAYLIST)