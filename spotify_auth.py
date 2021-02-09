import spotipy
import os
from dotenv import load_dotenv

load_dotenv()


def init_auth():
    """Connect to spotify to authenticate use of the users account"""

    oauth = spotipy.SpotifyOAuth(scope="playlist-modify-public", username=os.getenv("SPOTIPY_USERNAME"))
    token = oauth.get_access_token()


init_auth()