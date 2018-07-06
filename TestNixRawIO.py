from NixRawIO import NixRawIO
import numpy as np
import  collections


localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'


reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()
print(reader.segment_count(0))
print("abcbacb", reader.raw_annotations['blocks'][0]['segments'][1]['signals'][20])

r = reader.get_analogsignal_chunk(0,0,None,None,[1,2])
print(r)






