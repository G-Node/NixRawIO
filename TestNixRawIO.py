from NixRawIO import NixRawIO
import numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

x = [[1,2,3],[4,5,6]]
y = x[0]
y = np.array(y)
print(y)

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
r = reader.get_analogsignal_chunk(0,0,None,None,[1,2])
print(r)






