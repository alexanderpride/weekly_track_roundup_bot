import requests
import re
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


class Bot:

    def __init__(self):

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", username="Alexander Pride"))

    def getWTRDesc(self):

        playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c&key=" + os.getenv("API_KEY")

        res = requests.get(playlist_url)

        if res.status_code == 200:

            latest_video = res.json()["items"][0]
            print(latest_video)
            latest_video_description = latest_video["snippet"]["description"]

            print(latest_video_description)

            return latest_video_description

        else:

            print("Couldn't access the YouTube API")
            print("Status code", res.status_code)
            print(res.json())

    def getSongs(self, desc):

        songs = re.findall(r'.+ - .+', desc)

        return songs

    def getSearchTerm(self, song):
        """
        The format of the song desc can have a few different formats
        A couple of examples are...

        Anderson .Paak - Lockdown (Remix) ft. Noname, JID & Jay Rock
        Troye Sivan - Rager teenager!
        Machine Gun Kelly & blackbear - my ex's best friend

        There are three main categories I can determine in the song desc

        1: The artists that the song belongs to, on the left of the ' - '
        2: The name of the song, on the right of the ' - '
        3: The artists that feature on the song, after the 'ft.'
        """

        # Splits the song into category 1, and a joined category 2 and 3
        artists, song = song.split(" - ")
        artists = re.split(r'[,&]', artists)

        # Separate 2 and 3 into their own categories, and create a list of features
        if "ft." in song:
            song, features = song.split("ft.")
            features = re.split(r'[,&]', features)

        # Create a search string with the song name and artists included
        search_term = song + " "

        for artist in artists:
            search_term += artist

        return search_term

    def getSongIDs(self, songs):

        songIDs = []
        unfoundSongs = []
        print("Songs in Video Desc: " + str(len(songs)))

        for song in songs:

            # Replace all the parts that Spotify struggles to parse and format string for search

            print()
            print("Song searching for:")
            print(song)

            search_term = self.getSearchTerm(song)

            print("Using search term:")
            print(search_term)

            results = self.sp.search(search_term, type="track")

            tracks = results["tracks"]

            # CHeck if there was a song returned
            print("Song found:")
            if tracks["total"] > 0:

                trackItems = tracks["items"]

                print(trackItems[0]["artists"][0]["name"] + ", " + trackItems[0]["name"])

                songIDs.append(trackItems[0]["id"])

            else:

                unfoundSongs.append(song)

        print()
        print("Number of songs found by Spotify: " + str(len(songIDs)))
        print("Couldn't find:")

        for song in unfoundSongs:
            print(song)

        return songIDs

    def addToPlaylist(self, songIDs):

        """5kCKSF7HlIMjlIrStlCCra"""

        try:

            self.sp.user_playlist_replace_tracks(self.sp.current_user()["id"], "5kCKSF7HlIMjlIrStlCCra", songIDs)

        except:

            print("Error adding items to playlist")


def main():

    bot = Bot()
    desc = bot.getWTRDesc()
    songs = bot.getSongs(desc)
    songIDs = bot.getSongIDs(songs)
    bot.addToPlaylist(songIDs)


if __name__ == '__main__':
    main()
