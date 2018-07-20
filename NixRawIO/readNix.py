from __future__ import print_function

import nixio as nix

fileName = 'example-file.nix'
file = nix.File.open(fileName, nix.FileMode.ReadOnly)
print(file._data.get_data("Sample Data"))
print (file.blocks)
print(file.blocks[0])
print(file.blocks[0].groups[0].data_arrays[0])

dataarray = file.blocks[0].groups[0].data_arrays[0]
print(dataarray[0:100])

def Structure ():
    pass
