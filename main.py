from __future__ import absolute_import, print_function
import sys, os, signal, time

from spotify import fetchUserPlaylists, createPlaylistForUser
from parseUserPreference import UserTrackPreferences
from matrixFactor import matrixFactorize
from parseMusicData import TrackListingParser
from os import path

###############################################################################

utp = UserTrackPreferences("../MillionSongSubset/10000.txt",
                           "train_users_track_preferences.txt",
                           "user_track_preferences.txt",
                           "song_translation_echo_spotify.txt")
tlp = TrackListingParser("../MillionSongSubset/song_data.csv", "song_translation_RUNNING_CHANGE_echo_spotify.txt")

###############################################################################

def setup():
    global utp
    fin = open(path.relpath("spotify_app_credentials.txt"), 'r')
    devUserName, clientId, clientSecret, redirectUri = fin.readline().strip().split(' ')
    fin.close()
    utp.clientId = clientId
    utp.clientSecret = clientSecret
    utp.redirect_uri = redirectUri

    utp.username = raw_input("Enter Spotify user name [e-mail] >>  ")
    if utp.username == "":
        utp.username = devUserName

    fetchUserPlaylists(utp)

###############################################################################

def loadUserPref():
    global utp
    utp.parseTrainUserPref()
    utp.parseCurrentUserPref()
    utp.filterTrainUserPrefFile()

###############################################################################

def makePrediction():
    global utp
    matrixFactorize(utp)
    global tlp
    utp.translateRecommendationToTracks(tlp)
    createPlaylistForUser(utp)

###############################################################################

def run():
    loadUserPref()
    makePrediction()

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
    print ("1. Setup")
    print ("2. Run all")
    print ("")
    print ("3. Load MillionSongSet train users preferences")
    print ("4. Generate recommended playlist")
    print ("")
    print ("8. Fetch Spotify data for Echonest database")
    print ("9. Print status")
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
    '1': setup,
    '2': run,
    '3': loadUserPref,
    '4': makePrediction,
    '8': fetchSpotifyDataForEchonest,
    '9': printStatus,
    '0': exit,
}

###############################################################################

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    for x in sys.argv[1:]:
        if x == "init":
            setup()
            exit()

    main_menu()

###############################################################################
