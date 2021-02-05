import os
import tekore as tk

from dotenv import load_dotenv
from tekore.model import *
from tekore._auth import RefreshingToken

load_dotenv()

SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_CLIENT_ID = os.getenv("SPOTIFY_SECRET_CLIENT_ID")
REMOTE_SPOTIFY_REDIRECT_URI = os.getenv("REMOTE_SPOTIFY_REDIRECT_URI")
SPOTIFY_REDIRECT_URI = REMOTE_SPOTIFY_REDIRECT_URI


FILE = "token.cfg"


def spotify_login() -> RefreshingToken:
    conf = (SPOTIFY_CLIENT_ID, SPOTIFY_SECRET_CLIENT_ID, SPOTIFY_REDIRECT_URI)

    if os.path.exists(FILE):
        conf = tk.config_from_file(FILE, return_refresh=True)
        token = tk.refresh_user_token(*conf[:2], conf[3])
    else:
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
        tk.config_to_file(FILE, conf + (token.refresh_token,),)

    return token


def get_currently_playing(login_token):
    spotify_instance = tk.Spotify(login_token)
    currently_playing: CurrentlyPlaying = spotify_instance.playback_currently_playing()
    return track_details(currently_playing.item)

def track_details(record):
    big_image = record.images[0].url
    result = {}

    if record.type == "episode":
        result = {
            "type": "Episode",
            "name": record.name, 
            "url": record.href,
            "show": record.show.name, 
            "image": big_image
        }
    else:
        result = {
            "name": record.name,
            "artists": record.artists,
            "spotify_url": record.external_urls['spotify'] 
        }

    return result


if __name__ == "__main__":
    login_token = spotify_login()
    print(type(login_token))
    value = get_currently_playing(login_token)
    print(value)
