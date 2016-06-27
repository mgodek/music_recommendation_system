from __future__ import absolute_import, print_function
from os import path
from collections import defaultdict

###############################################################################

class UserTrackPreferences:
    def __init__(self, train_triplet_file_path = "", user_triplet_file_path=""):
        self.train_triplet_file_path  = train_triplet_file_path
        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)
        self.userIdxMap = dict()
        self.nextUserIndex = 0
        self.songIdxMap = dict()
        self.nextSongIndex = 0

        self.user_triplet_file_path = user_triplet_file_path

    ###########################################################################

    def parseCurrentUserPref(self):
        file_path = path.relpath("song_data_spotify_backup75k.csv")
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
                songId = trackTranslation[songIdSpotify]
                print("Checking %s" % songId)
                if songId in self.songIdxMap:
                    print("Found %s" % songId)

        fUserTrackPref.close()

    ###########################################################################

    def parseTrainUserPref(self):
        file_path = path.relpath(self.train_triplet_file_path)
        f = open(file_path, 'r')

        for line in f:
            userId, songId, playCount = line.strip().split('\t')

            ######### GENERATE INT INDEXES FOR SONG AND USER STRING IDS ########
            userIdx = 0
            if userId in self.userIdxMap:
                userIdx = self.userIdxMap[userId]
            else:
                userIdx = self.nextUserIndex
                self.nextUserIndex += 1
                self.userIdxMap[userId] = userIdx

            songIdx = 0
            if songId in self.songIdxMap:
                songIdx = self.songIdxMap[songId]
            else:
                songIdx = self.nextSongIndex
                self.nextSongIndex += 1
                self.songIdxMap[songId] = songIdx
            ######### GENERATE INT INDEXES FOR SONG AND USER STRING IDS ########

            if songIdx in self.global_track_like:
                self.global_track_like[songIdx] += int(playCount)
            else:
                self.global_track_like[songIdx] = int(playCount)

            self.user_track_like[userIdx][songIdx] = int(playCount)

        f.close()

    ###########################################################################

    def print(self):
        print("Global track likes:")
        for songId in self.global_track_like:
            print(songId, ':', self.global_track_like[songId])
        print("User track likes:")
        for userId in self.user_track_like:
            print(userId, ':')
            for songId in self.user_track_like[userId]:
                print(songId, '\t:', self.user_track_like[userId][songId])

    ###########################################################################