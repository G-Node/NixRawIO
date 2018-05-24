from NixRawIO import NixRawIO
import numpy as np
# np.set_printoptions(threshold=np.inf)

localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
#r = reader._rescale_spike_timestamp((np.array((2.4, 4.5))), dtype='float')
# r = reader._get_spike_timestamps(0,0,0,0.5,1)
r = reader._spike_count(0, 0, [0])
#print(reader)

print(r)