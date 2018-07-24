
from neo.io.basefromrawio import BaseFromRaw
from NixRawIO import NixRawIO
import nixio as nix
import numpy as np


class NixIOfr(NixRawIO, BaseFromRaw):

    name = 'Nix IO'
    _prefered_signal_group_mode = 'group-by-same-units'
    _prefered_units_group_mode = 'all-in-one'

    def __init__(self, filename):
        #file  = nix.File.open(filename, nix.FileMode.ReadWrite)
        #nb_blocks = file._block_count()
        #for i in range(nb_blocks):
            #del file.blocks[i]
        NixRawIO.__init__(self, filename=filename)
        BaseFromRaw.__init__(self, filename=filename)


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixIOfr(filename=localfile)
blk = reader.read_block(0, load_waveforms= True)
blk1 = reader.read_block(1, load_waveforms= True)
print(blk)
print(blk1)
print(blk.name)
print(blk.segments)
print(blk.segments[0].irregularlysampledsignals)  # rawio don't support irregularsignals
print('//////////////////////////////////////////////////')
for asig in blk.segments[0].analogsignals:
    print("asigname", asig.name)
    print(asig.shape)
print(blk.segments[0].analogsignals[1])
for asig in blk1.segments[0].analogsignals:
    print("asigname with block 2", asig.name)
    print(asig.shape)
print('------------------------------------------------')
for chx in blk.channel_indexes:
     print(chx.name)
     print(chx.channel_ids)
     print(chx.channel_names)
     print("index: {}:".format(chx.index))
     print ("===========================")
     for i, u in enumerate(chx.units):
         print(u.name)
         print(u.spiketrains)
         print(u.spiketrains[i].times)
         print(u.spiketrains[0].t_start)
         print(u.spiketrains[0].t_stop)
         for st in u.spiketrains:
             print(st.waveforms.units)
print(blk.segments[1].events[0].name)
print(blk.segments[0].epochs[0].name)


