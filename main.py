from __future__ import absolute_import, print_function
import sys, os, signal, time

from spotify import fetchUserPlaylists, createPlaylistForUser
from parseUserPreference import UserTrackPreferences
from matrixFactor import matrixFactorize
from parseMusicData import TrackListingParser
from os import path
from parseUserPreference import createPlaylistFromFile

###############################################################################

utp = UserTrackPreferences("../MillionSongSubset/10000.txt",
                           "train_users_track_preferences.txt",
                           "user_track_preferences.txt",
                           "user_favorites_translation.txt")#"song_translation_echo_spotify.txt")
tlp = TrackListingParser("../MillionSongSubset/song_data.csv", "song_translation_RUNNING_CHANGE_echo_spotify.txt")

###############################################################################

def setupUser(fetch=True):
    global utp
    fin = open(path.relpath("spotify_app_credentials.txt"), 'r')
    devUserName, clientId, clientSecret, redirectUri = fin.readline().strip().split(' ')
    fin.close()
    utp.clientId = clientId
    utp.clientSecret = clientSecret
    utp.redirect_uri = redirectUri

    utp.username = raw_input("Enter Spotify user name [e-mail, leave empty for default] >>  ")
    if utp.username == "":
        utp.username = devUserName

    if fetch == True:
        fetchUserPlaylists(utp)

###############################################################################

def loadUserPref():
    global utp
    print("Filter train data")
    t0 = time.clock()
#    utp.parseTrainUserPref()
    utp.parseCurrentUserPref()
    utp.filterTrainUserPrefFile()
    #utp.print()
    utp.clear()
    utp.parseTrainUserPref()
    utp.parseCurrentUserPref() # need to parse current user data again after filtering
    print("Time spent %s" % str(time.clock() - t0))
    utp.print()

###############################################################################

def makePrediction():
    global utp
    matrixFactorize(utp)
    global tlp
    utp.translateRecommendationToTracks(tlp)
    createPlaylistForUser(utp)

###############################################################################

def run():
    setupUser()
    loadUserPref()
    makePrediction()

###############################################################################

def createPlaylistFromFileMenu():
    global utp
    global tlp
    setupUser(False)
    createPlaylistFromFile(tlp, utp, "user_favorites.txt")

###############################################################################

def printStatus():
    global utp
    utp.print()

###############################################################################

def fetchSpotifyDataForEchonest():
    global tlp
    tlp.parseTrackListing()

###############################################################################

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    main_menu()

###############################################################################

def main_menu():
    global utp
    print ("")
    print (">>>> Running as user: %s <<<<" % utp.username)
    print ("Please choose the function you want to start:")
    print ("1. Run all [2 3 4]")
    print ("")
    print ("2. Setup user")
    print ("3. Load MillionSongSet train users preferences")
    print ("4. Generate recommended playlist")
    print ("")
    print ("7. Create Spotify playlist from file")
    print ("8. Fetch Spotify data for Echonest database [expert option]")
    print ("9. Print status[debug option]")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
 
    return

###############################################################################

menu_actions  = {}

###############################################################################

def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Wrong selection, please try again.")
            menu_actions['main_menu']()
    main_menu()

###############################################################################

menu_actions = {
    'main_menu': main_menu,
    '1': run,
    '2': setupUser,
    '3': loadUserPref,
    '4': makePrediction,
    '7': createPlaylistFromFileMenu,
    '8': fetchSpotifyDataForEchonest,
    '9': printStatus,
    '0': exit,
}

###############################################################################

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    #for x in sys.argv[1:]:
    #    if x == "noinit":
    #        main_menu()
    #    else:
    main_menu()

###############################################################################
