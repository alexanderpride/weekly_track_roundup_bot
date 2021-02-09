import spotipy
import os


def init_auth():
    """Connect to spotify to authenticate use of the users account"""

    spotipy.SpotifyOAuth(scope="playlist-modify-public", username=os.getenv("SPOTIPY_USERNAME"))


init_auth()