from NixRawIO import NixRawIO
import numpy as np
# np.set_printoptions(threshold=np.inf)

localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
#r = reader._rescale_spike_timestamp((np.array((2.4, 4.5))), dtype='float')
# r = reader._get_spike_timestamps(0,0,0,0.5,1)
r = reader.get_analogsignal_chunk(0,0,0, None, [3])
print("ch inx", reader.get_group_channel_indexes) # why all is unique? dtype and sr same but group id should be different!
print("ch id", reader.header['signal_channels']['group_id'])
#print(reader)
print(r)