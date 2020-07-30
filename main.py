import requests
import re
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def getChanel():
    # Gets theneedledrop's chanel and returns it

    req = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername=theneedledrop&key=" + os.getenv("API_KEY"))

    if req.status_code == 200:

        return req.json()["items"][0]

    else:

        return None


def getUploads(chanel):
    # Gets the playlistID for the chanels uploads so that the most recent video can be returned

    uploads_url = chanel["contentDetails"]["relatedPlaylists"]["uploads"]

    req = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId=' + uploads_url + '&key=' + os.getenv("API_KEY"))

    if req.status_code == 200:

        return req.json()["items"]


def getVideoDesc(uploads):
    # Returns the description from the Weekly Track Roundup video or None if it's not found

    for upload in uploads:

        if re.match(r'([Ww]eekly [Tt]rack [Rr]oundup)', upload["snippet"]["title"]):

            return upload["snippet"]["description"]

    return None


def getSongs(desc):

    songs = re.findall(r'.+ - .+', desc)

    return songs


def getSpotipyObject():

    scope = "playlist-modify-public"

    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username="Alexander Pride"))

def getSongIDs(sp, songs):

    songIDs = []
    print("Songs in Video Desc: " + str(len(songs)))

    for song in songs:

        # Replace all the parts that Spotify struggles to parse and format string for search

        _song = song.replace("&", "")
        _song = _song.replace("x", "")
        _song = _song.replace("ft.", "")
        _song = _song.replace(" ", "+")
        print(_song)

        results = sp.search(_song, type="track")

        tracks = results["tracks"]

        # CHeck if there was a song returned
        if tracks["total"] > 0:

            trackItems = tracks["items"]

            songIDs.append(trackItems[0]["id"])

            # TODO implement checking to always add the explicit song
            # # Check if there are two versions of the same track with and without explicit lyrics, if so add the one with
            # # explicit lyrics
            # if len(trackItems) == 2 and \
            #     trackItems[0]["name"] == trackItems[1]["name"] and \
            #     trackItems[0]["explicit"] != trackItems[1]["explicit"]:

        else:

            print("\n----------\n")
            print(song)
            print()
            print(tracks)
            print()
            print("\n----------\n")

    print("Songs found by Spotify: " + str(len(songIDs)))
    return songIDs



def main():

    sp = getSpotipyObject()
    chanel = getChanel()
    uploads = getUploads(chanel)
    desc = getVideoDesc(uploads)
    songs = getSongs(desc)

    songIDs = getSongIDs(sp, songs)



if __name__ == '__main__':
    main()
