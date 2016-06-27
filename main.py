from __future__ import absolute_import, print_function
import sys, os, signal, time

from spotify import spotifyTest, fetchUserPlaylists, createPlaylistForUser
from parseUserPreference import UserTrackPreferences
from matrixFactor import matrixFactorize
from parseMusicData import TrackListingParser

###############################################################################

utp = UserTrackPreferences()

###############################################################################

def setup():
    print("TODO")

###############################################################################

def createPlaylist():
    username = "" #TODO
    createPlaylistForUser(username)

###############################################################################

def fetchSpotifyDataForEchonest():
    spotifyTest() # TODO uncomment
#    tlp = TrackListingParser("../MillionSongSubset/song_data.csv","song_data_spotify.csv")
#    tlp.parseTrackListing()

###############################################################################

def fetchUserSpotifyData():
    username = raw_input("Enter Spotify user name [e-mail] >>  ")
    fetchUserPlaylists(username)

###############################################################################

def loadUserPref():
    global utp
    utp = UserTrackPreferences("../MillionSongSubset/100.txt","user_track_preferences.txt")
    utp.parseTrainUserPref()
    utp.parseCurrentUserPref()

###############################################################################

def makePrediction():
    matrixFactorize(utp)

###############################################################################

def printStatus():
    utp.print()

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
    print ("Please choose the function you want to start:")
    print ("1. Run")
    print ("2. Fetch Spotify data for Echonest database")
    print ("3. Load Million Song Set user preferences")
    print ("4. Fetch user playlist")
    print ("5. Matrix factorization")
    print ("6. Create recommended playlist")
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
    '1': run,
    '2': fetchSpotifyDataForEchonest,
    '3': loadUserPref,
    '4': fetchUserSpotifyData,
    '5': makePrediction,
    '6': createPlaylist,
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
