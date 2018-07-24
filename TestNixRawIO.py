from NixRawIO import NixRawIO
import  numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
print(reader.da_list['blocks'][0]['segments'][1]['data'][113][0:1200])
r = reader.get_analogsignal_chunk(1,1,None,None,[113,114,115,116,117])
print(r)
print(r.shape)
print("====================================================")
r = reader.get_spike_raw_waveforms(0,0,1, 0.1, None)
print(r.shape)
