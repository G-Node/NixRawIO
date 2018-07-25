from NixRawIO import NixRawIO
import  numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
x,y,z = reader.get_event_timestamps(0,0,0)
print(x)
r = reader.rescale_event_timestamp(x)
print(r)
print("====================================================")
r = reader.get_spike_raw_waveforms(0,0,0,None, None)
print(r.shape)
