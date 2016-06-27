from __future__ import absolute_import, print_function
from os import path
from collections import defaultdict
from parseMusicData import TrackListingParser

###############################################################################

class UserTrackPreferences:
    def __init__(self,
                 orig_train_triplet_file_path = "",
                 train_triplet_file_path = "",
                 user_triplet_file_path="",
                 echo_spotify_translation_file_path=""):
        self.orig_train_triplet_file_path = orig_train_triplet_file_path
        self.echo_spotify_translation_file_path = echo_spotify_translation_file_path

        self.username = ""
        self.clientId = ""
        self.clientSecret = ""
        self.redirect_uri = ""

        self.train_triplet_file_path  = train_triplet_file_path
        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)
        self.userIdxMap = dict()
        self.nextUserIndex = 0

        self.songIdxToEchoSongIdMap = dict()
        self.echoSongIdToIdxMap = dict()
        self.nextSongIndex = 0

        self.user_triplet_file_path = user_triplet_file_path

        self.user_feed_tracks = [] # use this set to filter recommended tracks, should not recommend known tracks
        self.user_feed_artists = []
        self.user_recommendations = dict()
        self.echo_user_recommended_tracks = []
        self.spotify_recommended_tracks = []

    ###########################################################################

    def parseCurrentUserPref(self):
        file_path = path.relpath(self.echo_spotify_translation_file_path)
        fTrackTranslation = open(file_path, 'r')
        trackTranslation = dict()
        for line in fTrackTranslation:
            song_id_echo, song_id_spotify = line.strip().split(':')
            trackTranslation[song_id_spotify] = song_id_echo
        fTrackTranslation.close()

        file_path = path.relpath(self.user_triplet_file_path)
        fUserTrackPref = open(file_path, 'r')
        for line in fUserTrackPref:
            userId, songIdSpotify, playCount = line.strip().split('\t')
            if songIdSpotify in trackTranslation:
                echoSongId = trackTranslation[songIdSpotify]
                self.user_feed_tracks.append(echoSongId)
                print("Checking %s" % echoSongId)
                if echoSongId in self.echoSongIdToIdxMap:
                    print("Found %s" % echoSongId)

        fUserTrackPref.close()

        # add artist for filtering
        fArtists = open(path.relpath("user_artist_preferences.txt"), 'r')
        for artist in fArtists:
            self.user_feed_artists.append(artist.replace("\n", ""))
        fArtists.close()
        print(self.user_feed_tracks)

    ###########################################################################

    def filterTrainUserPrefFile(self):
        file_path = path.relpath(self.orig_train_triplet_file_path)
        forig = open(file_path, 'r')

        user_feed_composite = self.user_feed_tracks + self.user_feed_artists
        goodTrainUsers = []
        for line in forig:
            if any(x in line for x in user_feed_composite):
                goodTrainUsers.append(line.split('\t', 1)[0])
                #print(line)

        forig.close()

        goodTrainUsers = set(goodTrainUsers)
        file_path = path.relpath(self.train_triplet_file_path)
        ffiltered = open(file_path, 'w')

        file_path = path.relpath(self.orig_train_triplet_file_path)
        forig = open(file_path, 'r')
        for line in forig:
            if any(x in line for x in goodTrainUsers):
                ffiltered.write(line)

        forig.close()

        ffiltered.close()

    ###########################################################################

    def parseTrainUserPref(self):
        fUserTrackPref = ""
        try:
            file_path = path.relpath(self.train_triplet_file_path)
            fUserTrackPref = open(file_path, 'r')
        except:
            print("File does not exist yet: %s Early return" % self.train_triplet_file_path)
            return

        for line in fUserTrackPref:
            userId, echoSongId, playCount = line.strip().split('\t')

            ######### GENERATE INT INDEXES FOR SONG AND USER STRING IDS ########
            userIdx = 0
            if userId in self.userIdxMap:
                userIdx = self.userIdxMap[userId]
            else:
                userIdx = self.nextUserIndex
                self.nextUserIndex += 1
                self.userIdxMap[userId] = userIdx

            songIdx = 0
            if echoSongId in self.echoSongIdToIdxMap:
                songIdx = self.echoSongIdToIdxMap[echoSongId]
            else:
                songIdx = self.nextSongIndex
                self.nextSongIndex += 1
                self.echoSongIdToIdxMap[echoSongId] = songIdx
                self.songIdxToEchoSongIdMap[songIdx] = echoSongId
            ######### GENERATE INT INDEXES FOR SONG AND USER STRING IDS ########

            if songIdx in self.global_track_like:
                self.global_track_like[songIdx] += int(playCount)
            else:
                self.global_track_like[songIdx] = int(playCount)

            self.user_track_like[userIdx][songIdx] = int(playCount)

        fUserTrackPref.close()

    ###########################################################################

    def translateRecommendationToTracks(self, tlp):
        self.echo_user_recommended_tracks = []
        for songIdx, songValue in self.user_recommendations.items():
            echoSongId = self.songIdxToEchoSongIdMap[songIdx]
            if echoSongId not in self.user_feed_tracks:
                self.echo_user_recommended_tracks.append(echoSongId)
            else:
                print("Skip %s which user knows" % echoSongId)

        #print(self.echo_user_recommended_tracks)
        self.spotify_recommended_tracks = tlp.getSpotifySongIds(self.echo_user_recommended_tracks)

    ###########################################################################

    def print(self):
        print("Username %s" % self.username)
        print("Global track likes:")
        for songId in self.global_track_like:
            print(songId, ':', self.global_track_like[songId])
        print("User track likes:")
        for userId in self.user_track_like:
            print(userId, ':')
            for songId in self.user_track_like[userId]:
                print(songId, '\t:', self.user_track_like[userId][songId])

    ###########################################################################