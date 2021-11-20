import requests
from bs4 import BeautifulSoup

def upload_tracks_from_vk(uri) -> list:
    soup = BeautifulSoup(requests.get(uri).text, 'lxml')
    text_content = soup.find_all('span')
    temp, tracks = list(), list()
    
    for span in text_content:
        if span.text:
            temp.append(span.text)
            
    for i in range(len(temp)):
        if '–' in temp[i]:
            tracks.append(temp[i - 1])
            
    return tracks

# for track in upload_tracks_from_vk('https://vk.com/music/playlist/170735510_38_018f4a24a2643650f3'):
    # print(track)