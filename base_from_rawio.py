
from neo.io.basefromrawio import BaseFromRaw
from NixRawIO import NixRawIO
import numpy as np


class NixIOfr(NixRawIO, BaseFromRaw):

    name = 'Nix IO'
    _prefered_signal_group_mode = 'group-by-same-units'
    _prefered_units_group_mode = 'all-in-one'

    def __init__(self, filename):
        NixRawIO.__init__(self, filename=filename)
        BaseFromRaw.__init__(self, filename=filename)


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'
reader = NixIOfr(filename=localfile)
blk = reader.read_block(0, load_waveforms= True)
print(blk)
#print(blk.name)
#print(blk.segments)
#print('-----------------',blk.segments[0].irregularlysampledsignals)
#for asig in blk.segments[0].analogsignals:
    #print("asigname", asig.name)
    #print(asig.shape)
for chx in blk.channel_indexes:
    print(chx.name)
    #print(chx.channel_ids)
    #print(chx.channel_names)
    #print("index: {}:".format(chx.index))
    for u in chx.units:
        print(u.name)
        print(u.spiketrains)
        print(u.spiketrains[0].times)
        print(u.spiketrains[0].t_start)
        print(u.spiketrains[0].t_stop)
print(blk.segments[0].events[0].name)


