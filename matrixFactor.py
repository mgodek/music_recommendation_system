###############################################################################

import numpy
import time

###############################################################################

def matrixFactorization(R, P, Q, K, epochMax=1000, alpha=0.0002, beta=0.02):
    Q = Q.T
    for step in xrange(epochMax):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
    return P, Q.T


###########################################################################

def createUserRow(utp):
    userRow = numpy.zeros(shape=(1, utp.nextSongIndex), dtype=float)

    for songId in utp.user_feed_artists_tracks + utp.user_feed_tracks:
        if songId in utp.echoSongIdToIdxMap:
            userRow[0][utp.echoSongIdToIdxMap[songId]] = 20 # hardcoded estimated playcount for current user
#        else:
#            print("Missing other user preference on %s" % songId)
    return userRow

###############################################################################

def createPreferenceMatrix(utp):
    R = numpy.zeros(shape=(utp.nextUserIndex+1, utp.nextSongIndex), dtype=float)

    print( "Create preference matrix R %d %d" %(utp.nextUserIndex+1, utp.nextSongIndex) )
    t0 = time.clock()
    for userId in utp.user_track_like:
        for songId in utp.user_track_like[userId]:
            R[userId][songId] = utp.user_track_like[userId][songId]

    print("Time spent %s" % str(time.clock() - t0))
    # add user row as last
    R[utp.nextUserIndex][:] = createUserRow(utp)
    return R

###############################################################################

def matrixFactorize(utp):
    R = createPreferenceMatrix(utp)

    N = len(R)
    M = len(R[0])
    K = 2

    P = numpy.random.rand(N,K).astype('f')
    Q = numpy.random.rand(M,K).astype('f')

    print("Matrix factorization")
    t0 = time.clock()
    nP, nQ = matrixFactorization(R, P, Q, K)
    print("Time spent %s" % str(time.clock() - t0))
#    print(nP)
#    print(nQ)
    nR = numpy.dot(nP, nQ.T)
    print(nR[utp.nextUserIndex][:]) # last user is the goal user
    songIdx = 0
    utp.user_recommendations_idxs.clear()
    for element in nR[utp.nextUserIndex]:
        #print(element)
        #print(songIdx)
        if element > 1: # greater than threshold TODO ask user?
            utp.user_recommendations_idxs[songIdx] = element
        else:
            print("Skip songIdx %d with value %d" %(songIdx, element))
        songIdx += 1

    print(utp.user_recommendations_idxs)

###############################################################################