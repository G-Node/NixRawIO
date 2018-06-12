from NixRawIO import NixRawIO
import numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'

reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
r = reader._get_analogsignal_chunk(0,2,None,None,[9])
print(r)






