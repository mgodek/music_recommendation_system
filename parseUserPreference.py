from __future__ import absolute_import, print_function
from os import path
from collections import defaultdict

###############################################################################

class UserTrackPreferences:
    def __init__(self, file_path = ""):
        self.file_path  = file_path
        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)
        self.userIdxMap = dict()
        self.nextUserIndex = 0
        self.songIdxMap = dict()
        self.nextSongIndex = 0

    ###########################################################################

    def parseUserPref(self):
        file_path = path.relpath(self.file_path)
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
                self.songIdxMap[songIdx] = songId
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