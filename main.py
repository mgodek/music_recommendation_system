from __future__ import absolute_import, print_function
import sys, os, signal, time

import numpy
from spotify import spotifyTest
from parseUserPreference import UserTrackPreferences
from matrixFactor import matrixFactorize

###############################################################################

utp = UserTrackPreferences()

###############################################################################

def setup():
    print("TODO")

###############################################################################

def readUserPlaylist():
    print( "TODO" )
    spotifyTest()

###############################################################################

def loadUserPref():
    global utp
    utp = UserTrackPreferences("../MillionSongSubset/100.txt")
    utp.parseUserPref()

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
    #sys.exit(0)
    main_menu()

###############################################################################

def main_menu():
    #os.system('clear')
    
    print ("Please choose the function you want to start:")
    print ("1. Run")
    print ("2. Spotify test")
    print ("3. Load Million Song Set user preferences")
    print ("4. Matrix factorization")
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
    '1': run,
    '2': readUserPlaylist,
    '3': loadUserPref,
    '4': makePrediction,
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
