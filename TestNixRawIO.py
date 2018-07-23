from NixRawIO import NixRawIO
import  numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()

r = reader.get_signal_size(0,0,[1,2,3])
print(r)
print("====================================================")

r = reader.get_spike_raw_waveforms(0,0,0)
print(r.shape)






