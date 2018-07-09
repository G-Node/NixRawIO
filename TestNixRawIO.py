from NixRawIO import NixRawIO
import  numpy as np
import  collections

list = [[1,2,3],[4,5,6],[7,8,9]]
list = np.array(list)
abc = list [:,[1,2]]
print(abc)

localfile = '/home/choi/PycharmProjects/Nixneo/neoraw.nix'


reader = NixRawIO(filename=localfile)
reader.__init__('neoraw.nix')
reader.parse_header()

r = reader.get_analogsignal_chunk(0,1,None,None,[0])
print(r)
print("====================================================")
r = reader.get_analogsignal_chunk(0,1,None,None,[10,11, 12])
print(r)






