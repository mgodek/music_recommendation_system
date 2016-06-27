from __future__ import absolute_import, print_function
import sys, os, signal, time

from spotify import fetchUserPlaylists, createPlaylistForUser
from parseUserPreference import UserTrackPreferences
from matrixFactor import matrixFactorize
from parseMusicData import TrackListingParser
from os import path

###############################################################################

utp = UserTrackPreferences()

###############################################################################

def setup():
    global utp
    utp = UserTrackPreferences("../MillionSongSubset/100.txt","user_track_preferences.txt")
    fin = open(path.relpath("spotify_app_credentials.txt"), 'r')
    devUserName, clientId, clientSecret, redirectUri = fin.readline().strip().split(' ')
    fin.close()
    utp.clientId = clientId
    utp.clientSecret = clientSecret
    utp.redirect_uri = redirectUri

    utp.username = raw_input("Enter Spotify user name [e-mail] >>  ")
    if utp.username == "":
        utp.username = devUserName

###############################################################################

def fetchUserSpotifyData():
    global utp
    fetchUserPlaylists(utp)

###############################################################################

def loadUserPref():
    global utp
    utp.parseTrainUserPref()
    utp.parseCurrentUserPref()

###############################################################################

def createPlaylist():
    global utp
    createPlaylistForUser(utp)

###############################################################################

def makePrediction():
    global utp
    matrixFactorize(utp)

###############################################################################

def printStatus():
    global utp
    utp.print()

###############################################################################

def fetchSpotifyDataForEchonest():
    tlp = TrackListingParser("../MillionSongSubset/song_data.csv","song_data_spotify.csv")
    tlp.parseTrackListing()

###############################################################################

def run():
    loadUserPref()
    makePrediction()

###############################################################################

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    main_menu()

###############################################################################

def main_menu():
    global utp
    print (">>>> Running as user: %s <<<<" % utp.username)
    print ("Please choose the function you want to start:")
    print ("1. Setup")
    print ("2. Run all")
    print ("3. Fetch Spotify data for Echonest database")
    print ("4. Load MillionSongSet train users preferences")
    print ("5. Fetch user spotify playlists")
    print ("6. Make matrix factorization")
    print ("7. Create recommended playlist")
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
    '3': fetchSpotifyDataForEchonest,
    '4': loadUserPref,
    '5': fetchUserSpotifyData,
    '6': makePrediction,
    '7': createPlaylist,
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
