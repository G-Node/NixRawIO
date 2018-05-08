import neo
import quantities as pq
import numpy as np
import nixio as nix
from neo.io import NixIO

block = neo.Block ()
chn_index = neo.ChannelIndex([0,1,2], channel_names= ["a","b","c"], channel_ids=[1, 2, 3])
block.channel_indexes.append(chn_index)
unit = neo.Unit(name= "x", description= "contain1st")
chn_index.units.append(unit)

seg = neo.Segment()
asig = neo.AnalogSignal(name="signal", signal=[1.1, 1.2, 1.5], units="mV", sampling_rate=1 * pq.Hz)
seg.analogsignals.append(asig)
asig2 = neo.AnalogSignal(name="signal2", signal=[1.1, 1.2, 2.5], units="mV", sampling_rate=1 * pq.Hz)
seg.analogsignals.append(asig2)
irasig = neo.IrregularlySampledSignal(name="irsignal", signal=np.random.random((100,2)), units="mV",
                                      times=np.cumsum(np.random.random(100) * pq.s))
seg.irregularlysampledsignals.append(irasig)
event = neo.Event(name="event", times= np.cumsum(np.random.random(10))* pq.ms, labels= ["event-"+str(idx) for idx in range(10)])
seg.events.append(event)
epoch = neo.Epoch(name="epoch", times= np.cumsum(np.random.random(10))* pq.ms, durations=np.random.random(10)*pq.ms, labels= ["epoch-"+str(idx) for idx in range(10)])
seg.epochs.append(epoch)
st = neo.SpikeTrain(name="train1", times=[0.21, 0.37, 0.53, 0.56], t_start=0 *pq.s, t_stop=2.4 *pq.s, units= pq.s, sampling_rate= 0.01)
seg.spiketrains.append(st)

block.segments.append(seg)
chn_index.analogsignals.append(asig)
chn_index.irregularlysampledsignals.append(irasig)
unit.spiketrains.append(st)


with NixIO("NeoMapping.nix", "ow") as nix_file:
    nix_file.write_block(block)


nf = nix.File.open("NeoMapping.nix")
for bl in nf.blocks:
    print(bl.name)
    for src in bl.sources:
        if src.type == "neo.channelindex":
            print("\t" + src.type)
            for csrc in src.sources:
                if csrc.type != "neo.channelindex": #do the same for nixrawio
                    print("\t\t csrc.type: {}".format(csrc.type))
                    continue
                index = csrc.metadata["index"]
                print("\t\t index: {}".format(index))
                name = csrc.metadata["neo_name"]
                print("\t\t name: {}".format(name))
                chanid = csrc.metadata["channel_id"]
                print("\t\t chanid: {}".format(chanid))
                print("-----")

    for grp in bl.groups:
        print(grp.type)
        for mt in grp.multi_tags:
            print(mt.type)
            print(mt.sources)
        for da in grp.data_arrays:
            print(da.type)
            print(da.sources)


nf.close()
