from __future__ import absolute_import, print_function
import spotipy

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