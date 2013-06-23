# build colisten matrix from triplet csv and save in mtx format

# usage:

# python colisten.py <infile> <outfile>

import scipy.sparse,scipy.io

import sys

import util


infile,outfile = sys.argv[1:]

colisten = scipy.sparse.lil_matrix((util.N_SONGS,util.N_SONGS))


for listens in util.songs_by_user(infile):

    for s , _ in listens:
        for t,_ in listens:
            colisten[s-1,t-1]+=1



scipy.io.mmwrite(file(outfile,'wb'),colisten)


