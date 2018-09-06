from nixrawio import NixRawIO
import  numpy as np
import  collections
import nixio as nix

list = [0,1,2,3,4,5,6,7,8]
list = np.array(list)
list_a = [0,1,2,3,4,5,6,7,8]
list_a = np.array(list_a)
assert list == list_a

localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'
file = nix.File.open('neoraw.nix', 'a')

d = file.blocks[0].data_arrays[0]
print(d.shape)
# reader = NixRawIO(filename=localfile)
#
# reader.__init__('neoraw.nix')
# reader.parse_header()
# r =reader.block_count()
# print(r)
# r = reader.get_analogsignal_chunk(0,0,None,None,[4,5,6,7,8])
# print(r)
# print("====================================================")
# r = reader.get_spike_raw_waveforms(0,0,0,None, None)
# print(r.shape)
