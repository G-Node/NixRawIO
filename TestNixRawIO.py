from NixRawIO import NixRawIO
import  numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
print(reader.file.blocks[0].groups[0].multi_tags)
r = reader.get_analogsignal_chunk(0,1,None,None,[113,117])
print(r)
print(r.shape)
print("====================================================")
r = reader.get_spike_raw_waveforms(0,0,1, 0.1, None)
print(r.shape)
