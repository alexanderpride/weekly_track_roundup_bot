import spotipy
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")

    mongoCli = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.t7nl0.mongodb.net")

    return mongoCli


def is_token_expired(token):

    return spotipy.is_token_expired(token)


def _get_token():

    mongoCli = connect_to_db()

    token_collection = mongoCli['tokenStore']['token']

    token = token_collection.find_one({}, {"_id": 0})

    return token


def create_cache(cache):

    token = _get_token()

    with open(cache, 'w+') as cache:

        cache.write(str(token).replace("\'", "\""))


def init_auth():
    """Connect to spotify to authenticate use of the users account"""

    mongoCli = connect_to_db()

    db = mongoCli['tokenStore']
    collection = db['token']

    oauth = spotipy.SpotifyOAuth(scope="playlist-modify-public", username=os.getenv("SPOTIPY_USERNAME"))
    token = oauth.get_access_token()

    if "token" not in db.list_collection_names() :

        collection.insert_one(token)
