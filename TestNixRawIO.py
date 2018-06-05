from NixRawIO import NixRawIO
import numpy as np
# np.set_printoptions(threshold=np.inf)

localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
#r = reader._rescale_spike_timestamp((np.array((2.4, 4.5))), dtype='float')
# r = reader._get_spike_timestamps(0,0,0,0.5,1)
r = reader.get_analogsignal_chunk(0,0, 0 , None, [4,5,6,7,8])
#print("ch inx", reader.get_group_channel_indexes) # why all is unique? dtype and sr same but group id should be different!
#reader._check_common_characteristics([1,2,3,4])
#print("ch id", reader.header['signal_channels']['sampling_rate'])
#print("dtype", reader.header['signal_channels']['dtype'])
#print(reader)
print(r)
