import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
from json import loads
from accessify import protected

class Uploader:
    def __init__(self, 
                 client_id, 
                 client_secret, 
                 redirect_uri, 
                 debug_mode = True):
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", 
                                                            client_id=client_id, 
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri))
        
        self.debug_mode = debug_mode

    @protected
    def cache(self):
        with open('.cache', 'r') as read_stream:
            content = read_stream.read()
            return loads(content)

    @protected
    def get_tracks_id(self, tracks) -> list:
        ready_tracks = list()
        
        for track in tracks:
            result = self.sp.search(q = 'track:' + track.get('track'), type = 'track')
            
            _ = result['tracks']['items']
                
            for elem in _:
                if elem.get('name').replace(' ', '').lower() == track.get('track').replace(' ', '').lower():
                    if elem['album']['artists'][0].get('name').lower() in track.get('artist').lower():
                        ready_tracks.append(elem.get('id'))
                        
                        if self.debug_mode:
                            print(f'Successfuly added {track} [+]')
                        
                        break
                else:
                    print(elem['album']['artists'][0].get('name'), '|', track.get('artist'), file = open('invalid.txt', 'a', encoding='utf-8'))
                    
                    if self.debug_mode:
                        print(f'Spotify has not track named {track} [-]')
                
        return ready_tracks

    @protected
    def get_titles_from_vk_playlist(self, uri) -> list:
        soup = BeautifulSoup(requests.get(uri).text, 'lxml')
        text_content = soup.find_all('span')
        temp, tracks = list(), list()
        
        for span in text_content:
            if span.text:
                temp.append(span.text)
                
        for i in range(len(temp)):
            if '–' in temp[i]:
                tracks.append({
                    'artist' : temp[i + 1],
                    'track' : temp[i - 1]
                })
                
        return tracks
    
    def upload_tracks_from_vk(self, uri, playlist_name):
        tracks_titles = self.get_titles_from_vk_playlist(uri)
        tracks = self.get_tracks_id(tracks_titles)
                
        playlists = self.sp.current_user_playlists().get('items')

        for playlist in playlists:
            if playlist.get('name') == playlist_name:
                    
               self.sp.playlist_add_items(playlist.get('id'), tracks, position=0)
               
        print(len(tracks))
               
    def clear_playlist(self, playlist_name):
        playlists = self.sp.current_user_playlists().get('items')
        
        for playlist in playlists:
            playlists = self.sp.current_user_playlists().get('items')
            if playlist.get('name') == playlist_name:
                tracks_in_this_playlist = list()
                for elem in loads(requests.get(playlist['tracks']['href'] + '?access_token=' + self.cache().get('access_token')).text)['items']:
                    tracks_in_this_playlist.append(elem['track'].get('id'))
                    
                self.sp.playlist_remove_all_occurrences_of_items(playlist.get('id'), tracks_in_this_playlist)