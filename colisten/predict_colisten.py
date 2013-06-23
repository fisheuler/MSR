# do prediction based on colisening matrix

# usage: python predict_coliste.py <mtxfile> <evalfile> <outfile>

# <outfile>

import sys

import itertools

import scipy.io

import numpy

import util

import time


mtxfile,evalfile,outfile = sys.argv[1:]

start = time.clock()

print " read colistenmatrix at time %f \n" % start

colisten = scipy.io.mmread(file(mtxfile)).tocsr()

read_end = time.clock()

timetoread = read_end-start

print " read completes at time %f \n" % read_end

print "it takes %f secs to read the colisten matrix " % timetoread

listens = colisten.diagonal()

listenranked = numpy.argsort(-listens)[:500]


predict_start = time.clock()

print " predict starts at %f :\n" % predict_start

with open(outfile,'w') as out:

    i = 0

    for history in util.songs_by_user(evalfile):

        i=i+1
        print " we are predict for %d user" % i
        
        songs,counts = zip(*history)

        sim = numpy.array(counts)[numpy.newaxis,:]*\
              colisten[numpy.array(songs)-1,:]


        simidxs = sim.nonzero()[1]

        srt = numpy.lexsort((-listens[simidxs],-sim[0,simidxs]))

        rankidxs = simidxs[srt]


        guess = []


        for s in rankidxs:
            if s+1 in songs:

                continue
            guess.append(str(s+1))

            if len(guess) == 500:break

        else:
            for s in listenranked:

                if s+1 in songs or s+1 in rankidxs:
                    continue
                guess.append(str(s+1))

                if len(guess) == 500: break

        


        out.write(' '.join(guess)+'\n') 

predict_end = time.clock()

print " predict ends at %f " % predict_end 


predict_time = predict_end - predict_start

print "it takes %f seconds to prediction " % predict_time




























                             

        


