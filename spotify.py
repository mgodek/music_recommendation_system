from __future__ import absolute_import, print_function
import spotipy
import sys
import spotipy
import spotipy.util as util
from os import path

###############################################################################

def spotifyTest():
    sp = spotipy.Spotify()

    results = sp.search(q='weezer', limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print('%d %s ' %(i, t['name']))

    results = sp.search(q='SOMPVQB12A8C1379BB', limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print('%d %s ' % (i, t['name']))

###############################################################################

def fetchSpotifySongId(artist, title):
    sp = spotipy.Spotify()

    results = sp.search(q='artist:'+artist+"+"+'track:'+title, limit=1, type='track')
    return results

###############################################################################

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print( "   %d %s %32.32s %s" % (i, track['id'], track['artists'][0]['name'], track['name']))

###############################################################################

def fetchUserPlaylist(username):
    fin = open(path.relpath("spotify_app_credentials.txt"), 'r')
    clientId, clientSecret, redirectUri = fin.readline().strip().split(' ')
    fin.close()

    print( "Login to Spotify as %s" % username )
    scope = 'playlist-read-private user-top-read user-library-read'
    token = util.prompt_for_user_token(client_id=clientId,
                                       client_secret=clientSecret,
                                       redirect_uri=redirectUri,
                                       username=username, scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        userId = sp.current_user()["id"]

        playlists = sp.user_playlists(userId)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == userId:
                print( playlist['name'])
                print( '  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(userId, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks) #TODO save songIds

    else:
        print("Can't get token for %s", username)

###############################################################################