from __future__ import absolute_import, print_function
from os import path
import string
import time
from spotify import fetchSpotifySongId

###############################################################################

class TrackListingParser:
    def __init__(self, file_path_in = "", file_path_out = ""):
        self.file_path_in  = file_path_in
        self.file_path_out = file_path_out

    ###########################################################################

    def parseTrackListing(self):
        fin = open(path.relpath(self.file_path_in), 'r')
        fout = open(path.relpath(self.file_path_out), 'w')

        fin.readline() # skip first line

        for line in fin:
            #time.sleep(2)
            song_id_echo, track_or, release, artist_or, year = line.strip().split(',')
            # remove punctuations
            exclude = set(string.punctuation)
            track = track_or.replace(" ", "+")
            release = ''.join(ch for ch in release if ch not in exclude)
            artist = artist_or.replace(" ", "+")
            year = ''.join(ch for ch in year if ch not in exclude)

            results = ""
            try:
                results = fetchSpotifySongId(artist, track)
            except:
                continue

            for tracks in results["tracks"]['items']:
                song_id_spotify = tracks["id"]
                print("%s %s" %(song_id_echo,song_id_spotify))
                fout.write(song_id_echo + ":" + song_id_spotify +'\n')
                break

        fin.close()
        fout.close()

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