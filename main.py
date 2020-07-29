import requests
import re

API_KEY = "AIzaSyCKQ6j3ccQ14zEgOfQ9Nk0GeJDd8QbimRE"


def getChanel():
    # Gets theneedledrop's chanel and returns it

    req = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&forUsername=theneedledrop&key=" + API_KEY)

    if req.status_code == 200:

        return req.json()["items"][0]

    else:

        return None


def getUploads(chanel):
    # Gets the playlistID for the chanels uploads so that the most recent video can be returned

    uploads_url = chanel["contentDetails"]["relatedPlaylists"]["uploads"]

    req = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId=' + uploads_url + '&key=' + API_KEY)

    if req.status_code == 200:

        return req.json()["items"]


def getVideoDesc(uploads):
    # Returns the description from the Weekly Track Roundup video or None if it's not found

    for upload in uploads:

        if re.match(r'([Ww]eekly [Tt]rack [Rr]oundup)', upload["snippet"]["title"]):

            return upload["snippet"]["description"]

    return None


def main():

    chanel = getChanel()
    uploads = getUploads(chanel)
    desc = getVideoDesc(uploads)
    print(desc)



if __name__ == '__main__':
    main()
