import spotipy
import os
from dotenv import load_dotenv
from configuration import CACHE_NAME

load_dotenv()

def is_token_expired(token):

    return spotipy.is_token_expired(token)


def create_cache(cache, token):


    with open(cache, 'w+') as cache:

        cache.write(str(token).replace("\'", "\""))


def init_auth():
    """Connect to spotify to authenticate use of the users account"""

    oauth = spotipy.SpotifyOAuth(scope="playlist-modify-public",
                                 username=os.getenv("SPOTIPY_USERNAME"),
                                 cache_path=CACHE_NAME)
    token = oauth.get_access_token()

    print(token)


if __name__ == '__main__':
    init_auth()
