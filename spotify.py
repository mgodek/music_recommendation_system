from __future__ import absolute_import, print_function
import spotipy
import sys
import spotipy
import spotipy.util as util
from os import path

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

def saveUserPreferences(userTracks, userArtists, userId):
    # save track ids to file
    userRating = "20"
    foutPref = open(path.relpath("user_track_preferences.txt"), 'w')
    for item in userTracks:
        foutPref.write(userId + '\t' + item + '\t' + userRating + '\n')
    foutPref.close()

    foutArtists = open(path.relpath("user_artist_preferences.txt"), 'w')
    userArtists = set(userArtists)
    for item in userArtists:
        foutArtists.write(item + '\n')
    foutArtists.close()

###############################################################################

def fetchUserPlaylists(utp):
    if utp.username == "":
        print("Fail. Need to run Setup first. Early return.")
        return

    print( "Login to Spotify as %s" % utp.username )
    scope = 'playlist-read-private user-top-read user-library-read playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(client_id=utp.clientId,
                                       client_secret=utp.clientSecret,
                                       redirect_uri=utp.redirect_uri,
                                       username=utp.username, scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        userId = sp.current_user()["id"]

        userArtists = []
        userTracks = []

        playlists = sp.user_playlists(userId)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == userId:
                print( playlist['name'])
                print( '  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(userId, playlist['id'], fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
                    # store songIds
                    for i, item in enumerate(tracks['items']):
                        userTracks.append(item['track']['id'])
                        #print(item['track']['artists'][0]['name'])
                        userArtists.append(item['track']['artists'][0]['name'].encode('utf-8'))

        saveUserPreferences(userTracks, userArtists, userId)

    else:
        print("Can't get token for %s", utp.username)

###############################################################################

def createPlaylistForUser(utp):
    if utp.username == "":
        print("Fail. Need to run Setup first. Early return.")
        return

    print( "Login to Spotify as %s" % utp.username )
    scope = 'playlist-read-private user-top-read user-library-read playlist-modify-private playlist-modify-public'
    token = util.prompt_for_user_token(client_id=utp.clientId,
                                       client_secret=utp.clientSecret,
                                       redirect_uri=utp.redirect_uri,
                                       username=utp.username, scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        userId = sp.current_user()["id"]

        playlistsInitData = sp.user_playlist_create(userId, "EINIS_MUSIC_RECOMMENDATION")
        playlistId = playlistsInitData['id']
        response = sp.user_playlist_add_tracks(user=userId, playlist_id=playlistId, tracks=["3xn1Ggm0X3EufcrKG5opJ3"]) #TODO
        #print(response)

    else:
        print("Can't get token for %s", utp.username)

###############################################################################
