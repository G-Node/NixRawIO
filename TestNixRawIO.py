from nixrawio import NixRawIO
import  numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
r = reader.get_analogsignal_chunk(0,0,None,None,[5,6,7,8])
print(r.shape)
print("====================================================")
r = reader.get_spike_raw_waveforms(0,0,0,None, None)
print(r.shape)
