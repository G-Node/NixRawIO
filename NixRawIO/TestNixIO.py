import neo

localfile = '/home/choi/PycharmProjects/Nixneo/example-file.nix'

reader = neo.io.NixIO(filename=localfile)

blks = reader.read(lazy=False)
print(blks)
# access to segments
for blk in blks:
    for seg in blk.segments:
        print(seg)
        #for asig in seg.analogsignals:
           #print(asig)
        for st in seg.spiketrains:
            print(st[0:10])