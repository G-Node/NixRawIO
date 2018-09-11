from nixrawio import NixRawIO
import  numpy as np
import  collections
import nixio as nix
import quantities as pq


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'
file = nix.File.open('neoraw.nix', 'a')

reader = NixRawIO(filename=localfile)
print(reader)
reader.parse_header()
r = reader.get_analogsignal_chunk(0,0,0,0,[0])
r = reader
print(r)
# print("====================================================")
# r = reader.get_spike_raw_waveforms(0,0,0,None, None)
# print(r.shape)

