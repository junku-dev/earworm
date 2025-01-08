import os
import time

from spotipy import Spotify, CacheFileHandler
from spotipy.oauth2 import SpotifyOAuth

def auth_user() -> Spotify:
    path:str = os.path.abspath("some/path/")
    return Spotify(auth_manager=SpotifyOAuth(
        cache_handler=CacheFileHandler(cache_path=path+"/path/to/cache"),
        client_id="",
        client_secret="",
        redirect_uri="",
        scope="user-read-recently-played user-top-read"
    ))

def recently_played_tracks() -> dict:
    sp: Spotify = auth_user()
    results: dict = sp.current_user_recently_played()

    ts:str = time.strptime(results['items'][0]['played_at'][:19], "%Y-%m-%dT%H:%M:%S")
    d:str = time.strftime("%m/%d/%Y", ts)

    track_info : dict = {
        "img":results['items'][0]['track']['album']['images'][1]['url'],
        "track":results['items'][0]['track']['album']['name'],
        "link":results['items'][0]['track']['external_urls']['spotify'],
        "artist":results['items'][0]['track']['album']['artists'][0]['name'],
        "popularity":results['items'][0]['track']['popularity'],
        "played_at": d
    }
    return track_info

def get_tops() -> dict:
    sp: Spotify = auth_user()
    results: dict = sp.current_user_top_tracks()

    top_tracks: dict = {}

    for i in range(20):
         top_tracks[i] = {
            "track_name":results['items'][i]['name'],
            "album_name":results['items'][i]['album']['name'],
            "artist":results['items'][i]['artists'][0]['name'],
            "album_art":results['items'][i]['album']['images'][1]['url']} 
         

    return top_tracks

if __name__ == "__main__":
    #test
    #print(recently_played_tracks())
    print(get_tops())