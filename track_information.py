class TrackInformation:

    def __init__(self, video_term, query, id, title=None, artist=None):

        self.video_term = video_term
        self.query = query
        self.id = id
        self.title = title
        self.artist = artist

    def __str__(self):

        term = self.video_term
        query = " |  QUERIED AS: '" + self.query + "'"
        found = " | FOUND AS: "

        if self.found_track():

            found += self.title + " by " + ", ".join(self.artist)

        else:

            term = "* " + term
            found += "NOT FOUND"

        return term + query + found

    def found_track(self):

        return self.id