from __future__ import absolute_import, print_function
import sys, os, signal, time
from spotify import spotifyTest

###############################################################################

def readUserPlaylist():
    print( "TODO" )
    spotifyTest()

###############################################################################
 
def setup():
    import sqlite3
    conn = sqlite3.connect('example.db')

###############################################################################

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    #sys.exit(0)
    main_menu()

###############################################################################

def main_menu():
    #os.system('clear')
    
    print ("Please choose the function you want to start:")
    print ("1. Run setup")
    print ("2. Spotify test")
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
    return

###############################################################################

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': setup,
    '2': readUserPlaylist,
    '0': exit,
}

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    global interactive
    interactive = False
    for x in sys.argv[1:]:
        if x == "init":
            setup()
            exit()

    main_menu()

###############################################################################
