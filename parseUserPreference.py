from __future__ import absolute_import, print_function
from os import path
from collections import defaultdict
from parseMusicData import TrackListingParser
from spotify import createPlaylistForUser

###############################################################################

class UserTrackPreferences:
    def __init__(self,
                 orig_train_triplet_file_path = "",
                 train_triplet_file_path = "",
                 user_triplet_file_path="",
                 echo_spotify_translation_file_path=""):
        self.orig_train_triplet_file_path = orig_train_triplet_file_path
        self.echo_spotify_translation_file_path = echo_spotify_translation_file_path
        self.createdPlaylistName = "EINIS_MUSIC_RECOMMENDATION"

        self.username = ""
        self.clientId = ""
        self.clientSecret = ""
        self.redirect_uri = ""

        self.train_triplet_file_path  = train_triplet_file_path
        self.user_triplet_file_path = user_triplet_file_path

        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)
        self.userIdxMap = dict()
        self.nextUserIndex = 0

        self.songIdxToEchoSongIdMap = dict()
        self.echoSongIdToIdxMap = dict()
        self.nextSongIndex = 0

        self.user_feed_tracks = [] # use this set to filter recommended tracks, should not recommend known tracks
        self.user_feed_artists = []
        self.user_feed_artists_tracks = [] # tracks which were added by artist filter
        self.user_recommendations_idxs = dict()
        self.echo_user_recommended_tracks = []
        self.spotify_recommended_tracks = []

    ###########################################################################

    def clear(self):
        self.global_track_like = dict()
        self.user_track_like = defaultdict(dict)
        self.userIdxMap = dict()
        self.nextUserIndex = 0

        self.songIdxToEchoSongIdMap = dict()
        self.echoSongIdToIdxMap = dict()
        self.nextSongIndex = 0

        self.user_feed_tracks = [] # use this set to filter recommended tracks, should not recommend known tracks
        self.user_feed_artists = []
        self.user_feed_artists_tracks = [] # tracks which were added by artist filter
        self.user_recommendations_idxs = dict()
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
#                print("Translated %s" % echoSongId)
#                if echoSongId in self.echoSongIdToIdxMap:
#                    print("Found %s" % echoSongId)
#            else:
#                print("Not found %s in translations" % songIdSpotify)

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

        goodTrainUsers = []
        for line in forig:
            if any(x in line for x in self.user_feed_tracks):
                goodTrainUsers.append(line.split('\t', 1)[0])
        forig.close()

        # TODO search in track database for additional echo song ids
        #if any(x in line for x in self.user_feed_artists):
        #    goodTrainUsers.append(line.split('\t', 1)[0])
        #    self.user_feed_artists_tracks.append(line.split('\t')[1])

        goodTrainUsers = set(goodTrainUsers) # make list unique
        file_path = path.relpath(self.train_triplet_file_path)
        ffiltered = open(file_path, 'w')

        file_path = path.relpath(self.orig_train_triplet_file_path)
        forig = open(file_path, 'r')
        for line in forig:
            if any(x in line for x in goodTrainUsers):
                userId, song_id_echo, playCount = line.strip().split('\t')
                if int(playCount) > 5: # using constant to limit size of train data
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
        for songIdx, songValue in self.user_recommendations_idxs.items():
            echoSongId = self.songIdxToEchoSongIdMap[songIdx]
            if echoSongId not in self.user_feed_tracks:
                if echoSongId not in self.user_feed_artists_tracks:
                    self.echo_user_recommended_tracks.append(echoSongId)
                else:
                    print("Skipping %s which user is familiar (maybe)" % echoSongId)
            else:
                print("Skip %s which user knows" % echoSongId)

        #print(self.echo_user_recommended_tracks)
        self.spotify_recommended_tracks = tlp.getSpotifySongIds(self.echo_user_recommended_tracks)

    ###########################################################################

    def print(self):
        print("Username %s" % self.username)

        print( "self.nextUserIndex %d" % self.nextUserIndex )
        print( "self.nextSongIndex %d" % self.nextSongIndex )
        #print( "self.user_feed_artists_tracks %s" % str(self.user_feed_artists_tracks) )
        print( "self.user_feed_tracks %d" % len(self.user_feed_tracks))
        #print( "self.user_feed_artists %s" % str(self.user_feed_artists))

        #print("Global track likes:")
        #for songId in self.global_track_like:
        #    print(songId, ':', self.global_track_like[songId])
        #print("User track likes:")
        #for userId in self.user_track_like:
        #    print(userId, ':')
        #    for songId in self.user_track_like[userId]:
        #        print(songId, '\t:', self.user_track_like[userId][songId])

###########################################################################

def createPlaylistFromFile(tlp, utp, filepath):
    fUserTrackPref = ""
    try:
        file_path = path.relpath(filepath)
        fUserTrackPref = open(file_path, 'r')
    except:
        print("File does not exist yet: %s Early return" % filepath)
        return

    echo_songs = []
    for line in fUserTrackPref:
        echoSongId = line.strip().split(',', 1)[0]
        echo_songs.append(echoSongId)

    spotify_songs = tlp.getSpotifySongIds(echo_songs,"user_favorites_translation.txt")
    backup1 = utp.spotify_recommended_tracks
    utp.spotify_recommended_tracks = spotify_songs
    backup2 = utp.createdPlaylistName
    utp.createdPlaylistName = "EINIS_USER_FAVOURITES"
    createPlaylistForUser(utp)

    utp.spotify_recommended_tracks = backup1
    utp.createdPlaylistName = backup2

    fUserTrackPref.close()

###########################################################################