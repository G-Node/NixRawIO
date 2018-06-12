from NixRawIO import NixRawIO
import numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()

r = reader.get_analogsignal_chunk(0,0, 0 , None, [4,5,6,7,8])
print(r)
print(reader.header["event_channels"]['type'][0])


a = {1: "a", 2: "b", 3: "c"}

abc, = np.nonzero(a[2] == "b")

print(abc)

print("---------------")
print(reader.raw_annotations['signal_channels'][0].keys())
# print(reader.get_signal_size(0,0,[1,2,3,4,5])) => fail because of different characteristics
all_channels = reader.header['signal_channels']
channel_indexes = np.arange(all_channels.size, dtype=int)
channels = all_channels[channel_indexes]
groups = collections.OrderedDict()
all_units = np.unique(channels['units'])
for i, unit in enumerate(all_units):
    ind_within, = np.nonzero(channels['units'] == unit)
    print("diuni", ind_within)
    ind_abs = channel_indexes[ind_within]
    print("ind_abs", ind_abs)
    groups[i] = (ind_within, ind_abs)
    print(i)



