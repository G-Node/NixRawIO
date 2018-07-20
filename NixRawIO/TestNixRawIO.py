from NixRawIO import NixRawIO
import numpy as np

localfile = '/home/choi/PycharmProjects/Nixneo/example-file.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('NeoMapping.nix')
reader.parse_header()
r = reader._rescale_spike_timestamp((np.array((2.4, 4.5))), dtype='float')
# r = reader._get_spike_timestamps(0,0,0,0.5,1)
print(reader)

print(r)