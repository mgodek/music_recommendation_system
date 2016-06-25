from __future__ import absolute_import, print_function
import sys, os, signal, time

from spotify import spotifyTest
from parseUserPreference import UserTrackPreferences

###############################################################################

utp = UserTrackPreferences()

###############################################################################

def setup():
    print("TODO")

###############################################################################

def matrixFactorize():
    print( "TODO" )

###############################################################################

def readUserPlaylist():
    print( "TODO" )
    spotifyTest()

###############################################################################

def loadUserPref():
    global utp
    utp = UserTrackPreferences("../MillionSongSubset/train_triplets.txt")
    utp.parseUserPref()

###############################################################################

def printStatus():
    utp.print()

###############################################################################

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #sys.exit(0)
    main_menu()

###############################################################################

def main_menu():
    #os.system('clear')
    
    print ("Please choose the function you want to start:")
    print ("1. Spotify test")
    print ("2. Load Million Song Set user preferences")
    print ("3. Matrix factorization")
    print ("9. Print status")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
 
    return

###############################################################################

menu_actions  = {}

###############################################################################

def exec_menu(choice):
    #os.system('clear')
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
    '1': readUserPlaylist,
    '2': loadUserPref,
    '3': matrixFactorize,
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
