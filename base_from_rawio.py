
from neo.io.basefromrawio import BaseFromRaw
from NixRawIO import NixRawIO


class NixIOfr(NixRawIO, BaseFromRaw):
    """
    This IO reads .nev/.nsX files of the Blackrock
    (Cerebus) recording system.
    """
    name = 'Nix IO'

    def __init__(self, filename):
        NixRawIO.__init__(self, filename=filename)
        BaseFromRaw.__init__(self, filename=filename, group_mode = 'group-by-same-units') #


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'
reader = NixIOfr(filename=localfile)
# r = reader._get_analogsignal_chunk(0,0,0, None, [0])
blk = reader.read_block(0) # seems like only CI2 is read (5 indexes)
print(blk)
#print(blk.name)
#print(blk.segments)
print('-----------------',blk.segments[0].analogsignals)
#for asig in blk.segments[0].analogsignals:
    #print(asig.name)
    #print(asig.shape)
for chx in blk.channel_indexes:
    print(chx.name)
    print(chx.channel_ids)
    print(chx.channel_names)