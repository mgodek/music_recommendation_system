from __future__ import absolute_import, print_function
from os import path
from collections import defaultdict

class UserTrackPreferences:
    def __init__(self, file_path = ""):
        self.file_path  = file_path
        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)

    def parseUserPref(self):
        file_path = path.relpath(self.file_path)
        f = open(file_path, 'r')

        for line in f:
            userId, songId, playCount = line.strip().split('\t')
            if songId in self.global_track_like:
                self.global_track_like[songId] += 1
            else:
                self.global_track_like[songId] = 1

            if userId in self.user_track_like:
                if songId in self.user_track_like[userId]:
                    self.user_track_like[userId][songId] += 1
                else:
                    self.user_track_like[userId][songId] = 1
            else:
                self.user_track_like[userId][songId] = 1

        f.close()

    def print(self):
        print("Global track likes:")
        for songId in self.global_track_like:
            print(songId, ':', self.global_track_like[songId])
        print("User track likes:")
        for userId in self.user_track_like:
            print(userId, ':')
            for songId in self.user_track_like[userId]:
                print(songId, '\t:', self.user_track_like[userId][songId])