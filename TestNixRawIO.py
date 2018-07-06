from NixRawIO import NixRawIO
import numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'


reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
print("abcbacb", reader.raw_annotations['blocks'][0:2]['segments'][:])

r = reader.get_analogsignal_chunk(0,0,None,None,[1,2])
print(r)






