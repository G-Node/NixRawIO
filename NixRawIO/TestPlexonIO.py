# -*- coding: utf-8 -*-
"""
This is an example for reading files with neo.io
"""

import urllib

import neo


localfile = '/home/choi/Downloads/File_plexon_3.plx'


# create a reader
reader = neo.io.PlexonIO(filename=localfile)
# read the blocks
blks = reader.read(lazy=False)
print(blks)
# access to segments
for blk in blks:
    for seg in blk.segments:
        print(seg)
        #for asig in seg.analogsignals:
           #print(asig)
        for st in seg.spiketrains:
            print(st[0:10])
