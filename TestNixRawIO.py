from nixrawio import NixRawIO
import  numpy as np
import  collections
import nixio as nix
import quantities as pq


localfile = '/home/choi/PycharmProjects/Nixneo/test_case.nix'
file = nix.File.open('test_case.nix', 'a')

list = ['a','b','c', 'd']
array = np.array(list)
print(array)
arrays = np.array(array)
arrays = arrays.astype("S")
print(arrays)

if np.all(arrays == array):
    print('abc')

d = file.blocks[0].name
print(d)
reader = NixRawIO(filename=localfile)
x = 10 * pq.ms + np.cumsum(np.array([0,1,2,3,4])) * pq.ms
print(x)
reader.parse_header()
r = reader._get_event_timestamps(0,0,0,0,1000)
print(r)
# print("====================================================")
# r = reader.get_spike_raw_waveforms(0,0,0,None, None)
# print(r.shape)
