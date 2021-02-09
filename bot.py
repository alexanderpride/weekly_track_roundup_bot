from __future__ import print_function

import os
import spotipy
import smtplib
import ssl

from googleapiclient.discovery import build
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from email.mime.text import MIMEText

from configuration import *

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class Bot:

    def __init__(self):
        """Connect and validate to the APIs necessary for running"""

        # Set up for accessing the youtube API
        api_service_name = "youtube"
        api_version = "v3"
        youtube = build(api_service_name,
                        api_version,
                        developerKey=os.getenv("YOUTUBE_API_KEY"))

        self.youtube = youtube

        # Set up for Spotipy

        self.spotipy = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public",
                                                                 username=os.getenv("SPOTIPY_USERNAME")))


    def __get_video__(self, playlist_id):
        """ Collect the latest video from the Weekly Track Roundup playlist and then
        return the description from the video, where the songs are listed"""

        request = self.youtube.playlistItems().list(
            part="snippet",
            maxResults=1,
            playlistId=playlist_id
        )
        response = request.execute()

        video = response['items'][0]['snippet']

        return video

    def __is_new_video__(self, video):
        """Check if the video is the latest video. If the video is new update the upload time and returns true,
        else just returns false"""

        flag = False

        if os.path.exists(UPLOAD_TIME_FILE):

            with open(UPLOAD_TIME_FILE, 'r') as upload_file:

                if upload_file.read() < video['publishedAt']:

                    self.__update_upload_time__(video)

                    flag = True

        else:

            self.__update_upload_time__(video)

            flag = True

        return flag

    @staticmethod
    def __update_upload_time__(video):

        with open(UPLOAD_TIME_FILE, 'w+') as upload_file:

            upload_file.write(video['publishedAt'])

    @staticmethod
    def __process_description__(video):
        """Collects all the songs listed in the video's description and formats them to
        be easily found by Spotify. Returns a list of tuples containing how the song was
        listed in the description and how it has been processed for spotify
        """

        description = video['description']

        tracks = get_tracks(description)
        processed_tracks = []

        for track in tracks:

            processed_track = process_track(track)
            processed_tracks.append((track, processed_track))

        return processed_tracks

    def __get_tracks_information__(self, processed_tracks):
        """Query Spotify's database to collect the track and track ID"""

        items = []

        for processed_track in processed_tracks:

            video_term, q = processed_track

            result = self.spotipy.search(q=q, type='track')

            tracks = result["tracks"]

            if tracks["total"] > 0:

                track = tracks["items"][0]

                id = track["id"]
                title = track["name"]
                artist = [artist["name"] for artist in track["artists"]]

                items.append(TrackInformation(video_term, q, id, title, artist))

            else:

                items.append(TrackInformation(video_term, q, None))

        return items

    def __update_playlist__(self, tracks_information):
        """Replace tracks in playlist with the new tracks"""

        ids = [track.id for track in tracks_information if track.id]

        self.spotipy.user_playlist_replace_tracks(self.spotipy.current_user()["id"],
                                                  os.getenv("PLAYLIST_ID"), ids)

    def __send_email__(self, tracks_information, video):
        """Send email to hoster describing the tracks that were found and not found.

        The email subject line and body comes from the construct_email function in the configuration file"""

        subject, email_body = construct_email(tracks_information, video)

        message = MIMEText(email_body, 'plain')
        message['to'] = TO_EMAIL_ADDRESS
        message['from'] = FROM_EMAIL_ADDRESS
        message['subject'] = subject

        context = ssl.create_default_context()

        try:

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:

                username, password = os.getenv("GMAIL_USERNAME"), os.getenv("GMAIL_PASSWORD")
                server.login(username, password)

                server.sendmail(FROM_EMAIL_ADDRESS, TO_EMAIL_ADDRESS, message.as_string())

        except Exception as e:

            print("Unexpected error:", e)

    def run(self):

        video = self.__get_video__(YOUTUBE_PLAYLIST_ID)

        if self.__is_new_video__(video):

            processed_tracks = self.__process_description__(video)

            tracks_information = self.__get_tracks_information__(processed_tracks)

            self.__update_playlist__(tracks_information)
            self.__send_email__(tracks_information, video)
            print("Code run at " + str(datetime.datetime.now()))


    def force_run(self):

        video = self.__get_video__(YOUTUBE_PLAYLIST_ID)

        processed_tracks = self.__process_description__(video)

        tracks_information = self.__get_tracks_information__(processed_tracks)

        self.__update_playlist__(tracks_information)
        self.__send_email__(tracks_information, video)
        print("Code run at " + str(datetime.datetime.now()))

