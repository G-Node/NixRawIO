
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
# r = reader._get_analogsignal_chunk(0,0,0, None, [0])
blk = reader.read_block(0) # seems like only CI2 is read (5 indexes)
print(blk)
#print(blk.name)
#print(blk.segments)
#print('-----------------',blk.segments[0].analogsignals)
#for asig in blk.segments[0].analogsignals:
    #print(asig.name)
    #print(asig.shape)
#print("xxxxxxxxxxxxxxxxxxxxxxxxx", blk.segments[0].units)
for chx in blk.channel_indexes:
    print(chx.name)
    print(chx.channel_ids)
    print(chx.channel_names)
    print("index: {}:".format(chx.index))
    #for u in chx.units:
        #print(u.spiketrains)
print(blk.segments[0].epochs) # epoch is missing, duration/times
x = reader._make_signal_channel_subgroups(np.array([0,1,2,3,4,5,6,7,8])).items()
print(x)
