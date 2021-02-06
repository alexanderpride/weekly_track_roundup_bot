import re
import datetime

from string import Template
from track_information import TrackInformation


YOUTUBE_PLAYLIST_ID = "PLP4CSgl7K7or84AAhr7zlLNpghEnKWu2c"
UPLOAD_TIME_FILE = "uploadfile"
EMAIL_MESSAGE_TEMPLATE = "email_template"
TO_EMAIL_ADDRESS = "alexandercpride@gmail.com"
FROM_EMAIL_ADDRESS = "weeklytrackroundupbot@gmail.com"


def get_tracks(description: str) -> list[str]:
    """
    Get video description and return list of songs in description

    Gets all the tracks from the description and returns them as a list.
    This function is given the video description and returns a list of the tracks
    found in the description, with each track being in a string format.
    I found a simple regular expression rather helpful for this."""

    tracks = re.findall(r'.+ - .+', description)

    return tracks


def process_track(track: str) -> str:
    """
    Format track in video description for the spotify search and return formatted string

    Gets given a track as a string, and then reformats the string to better suit the
    spotify search criteria, found at https://developer.spotify.com/documentation/web-api/reference/#category-search

    Of note, this service uses spotipy, and uses their search function. In doing so
    it is not necessary to encode spaces.

    This function returns the query as a string.

    --------------------------------------------------------------------------

    Takes a track from the description and formats it for searching on Spotify

    A few examples of songs in the description of a Weekly Track Roundup video

    Anderson .Paak - Lockdown (Remix) ft. Noname, JID & Jay Rock

    Guapdad 4000 - Alpha (Remix) ft. Bfb Da Packman

    JPEGMAFIA - Super Tuesday!

    Troye Sivan & Kacey Musgraves - Easy ft. Mark Ronson

    Jeremih & Chance the Rapper - Who's to Say / The Return

    The artists and the track are separated by a -
    Features come after the song name. This can be a troubling piece of information
    as some artists do not list the feature on Spotify
    Artists that share a track are separated by an &
    Information between brackets is meaningless to Spotify and can be removed
    A / between the song names indicates that they are seperate songs"""


    try:

        artists, title = track.split(" - ")
        artists = re.split(r' [,&] ', artists)

        # Remove any parenthesis containing useless info
        if title.find('(') > 0:
            title = title[0:title.find('(')] + title[title.find(')') + 1:]

        # Check for features
        if "ft." in title:

            title, features = title.split("ft.")
            features = re.split(r' [,&] ', features)

            artists = artists + features

        track_query = "track:" + title
        artist_query = "artist:"

        for artist in artists:

            artist_query += artist + " "

        q = artist_query + track_query

        return q

    except ValueError:

        return ""


def construct_email(tracks_information: list[TrackInformation], video: dict) -> (str, str):
    """
    Format information from the running of the program and return an email subject line and body

    In the running of the program, slight differences in video descriptions can change the
    way that the information is processed. The implementer may also want different information
    to be present in the email that is sent. The user has the opportunity to use the information
    that has been passed through the program to construct their email.
    """

    subject = "Weekly Track Roundup for " + str(datetime.date.today())
    songs = "\n\n".join([str(t) for t in tracks_information])
    unfound_songs = "\n".join([t.video_term for t in tracks_information if not t.id])
    num_songs_uploaded = len(tracks_information)
    num_songs_found = num_songs_uploaded - len([t.video_term for t in tracks_information if not t.id])

    substitutions = {

        'title': video['title'],
        'video_upload_time': video['publishedAt'],
        'bot_run_time': str(datetime.datetime.now()),
        'num_songs_uploaded': num_songs_uploaded,
        'num_songs_found': num_songs_found,
        'songs': songs,
        'unfound_songs': unfound_songs

    }

    with open(EMAIL_MESSAGE_TEMPLATE, 'r') as email_template:

        raw_template = email_template.read()

        template = Template(raw_template).substitute(substitutions)

    return subject, template
