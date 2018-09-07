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
array
arrays = np.array([], dtype='S')
print(arrays)

if np.all(arrays == array):
    print('abc')

x = np.array([1,2,3,4])
y =x/4
print(y)
d = file.blocks[0].name
print(d)
reader = NixRawIO(filename=localfile)
x = 10 * pq.ms + np.cumsum(np.array([0,1,2,3,4])) * pq.ms
print(x)
reader.parse_header()
r = reader._get_event_timestamps(0,0,0,0,1000)
print(r)
x = reader._rescale_event_timestamp(r[0])
print(x)
# print("====================================================")
# r = reader.get_spike_raw_waveforms(0,0,0,None, None)
# print(r.shape)
