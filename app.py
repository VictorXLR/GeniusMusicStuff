import os

import dotenv
import requests
from bs4 import BeautifulSoup

dotenv.load_dotenv()

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

SEARCH_ENDPOINT = "api.genius.com/search"
SONG_ENDPOINT = "api.genius.com/songs/"
USER_ENDPOINT = "api.genius.com/account"


base_url = "http://api.genius.com"
headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}

song_title = "ONE WATCH"
artist_name = "Gunna"


def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html("script")]
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics


if __name__ == "__main__":
    search_url = base_url + "/search"
    data = {"q": song_title}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        hit_artist_name = hit["result"]["primary_artist"]["name"]
        if hit_artist_name.upper() == artist_name.upper():
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        print(lyrics_from_song_api_path(song_api_path))
