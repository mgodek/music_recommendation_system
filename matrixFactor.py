###############################################################################

import numpy

###############################################################################

def matrixFactorization(R, P, Q, K, epochMax=5000, alpha=0.0002, beta=0.02):
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

###############################################################################

def createPreferenceMatrix(userTrackPreference):
    R = numpy.zeros(shape=(userTrackPreference.nextUserIndex, userTrackPreference.nextSongIndex), dtype=float)
    for userId in userTrackPreference.user_track_like:
        for songId in userTrackPreference.user_track_like[userId]:
            R[userId][songId] = userTrackPreference.user_track_like[userId][songId]
    return R

###############################################################################

def matrixFactorize(userTrackPreference):
    print( "matrixFactorize" )
    R = createPreferenceMatrix(userTrackPreference)

    N = len(R)
    M = len(R[0])
    K = 2

    P = numpy.random.rand(N,K).astype('f')
    Q = numpy.random.rand(M,K).astype('f')

    nP, nQ = matrixFactorization(R, P, Q, K)
#    print(nP)
#    print(nQ)
    nR = numpy.dot(nP, nQ.T)
    print(R[0])
    print(nR[0]) # TODO specify which user is the goal user
    songIdx = 0
    userTrackPreference.user_recommendations.clear()
    for element in nR[0]:
        #print(element)
        #print(songIdx)
        userTrackPreference.user_recommendations[songIdx] = element # TODO add only chosen
        songIdx += 1

    print(userTrackPreference.user_recommendations)

###############################################################################