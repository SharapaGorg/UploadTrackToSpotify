from utils import Uploader
from config import settings

#https://developer.spotify.com/dashboard/applications/ - create app and copy client_id and client_secret

BASE_PLAYLIST = 'FONK!!!FONK!!!FONK'

uploader = Uploader(settings.get('client_id'), 
                    settings.get('client_secret'), 
                    settings.get('redirect_uri'), 
                    debug_mode=False)

uploader.upload_tracks_from_vk('https://vk.com/music/playlist/170735510_38_018f4a24a2643650f3', BASE_PLAYLIST)