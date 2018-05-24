from neo import (Block, Segment,
                 AnalogSignal, IrregularlySampledSignal,
                 Event, Epoch, SpikeTrain,
                 ChannelIndex, Unit)
from neo.io.nixio import NixIO

import numpy as np
import quantities as pq


nsegments = 1

block = Block("nix-raw-block", description="The root block")

for idx in range(nsegments):
    seg = Segment("seg-ex{}".format(idx),
                  description="Segment number {}".format(idx))
    block.segments.append(seg)



    # Generate 3 fake data signals using numpy's random function
    # The shapes of the arrays are arbitrary
    data_a = np.random.random((300, 1)) # make the shape all the same, to make sure array generation is good
    # not sure if it is the general case
    data_b = np.random.random((1200, 3))
    data_c = np.random.random((8000, 5))
    nchannels = data_a.shape[1] + data_b.shape[1] + data_c.shape[1]
    nchannels = 3

    sampling_rate = pq.Quantity(10, "Hz")

    indexes = np.arange(nchannels)
    for ch in range(nchannels):
        chx = ChannelIndex(name="channel-{}".format(idx + ch),
                           index=indexes,
                           channel_names=[chr(ord("a") + i) for i in indexes],
                           channel_ids=indexes + 1)

        block.channel_indexes.append(chx)

    for didx, data in enumerate((data_a, data_b, data_c)):
        asig = AnalogSignal(name="Seg {} :: Data {}".format(idx, didx),
                            signal=data, units="mV",
                            sampling_rate=sampling_rate)
        seg.analogsignals.append(asig)
        block.channel_indexes[didx].analogsignals.append(asig)

    # random sampling times for data_b
    irsigdata = np.random.random((1200, 2))
    itimes = np.cumsum(np.random.random(1200))

    # Create one AnalogSignal and one IrregularlySampledSignal
    isig = IrregularlySampledSignal(name="Sampled data", signal=irsigdata,
                                    units="nA",
                                    times=itimes, time_units="ms")
    seg.irregularlysampledsignals.append(isig)

    # Event, Epoch, SpikeTrain
    tstart = 10 * pq.ms
    event_times = tstart + np.cumsum(np.random.random(5)) * pq.ms
    event = Event(name="Seg {} :: Event".format(idx),
                  times=event_times,
                  labels=["A", "B", "C", "D", "E"])
    seg.events.append(event)

    epoch_times = tstart + np.cumsum(np.random.random(3)) * pq.ms
    epoch = Epoch(name="Seg {} :: Epoch".format(idx),
                  times=epoch_times,
                  durations=np.random.random(3)*pq.ms,
                  labels=["A+", "B+", "C+"])
    seg.epochs.append(epoch)

    st_times = tstart + np.cumsum(np.random.random(10)) * pq.ms
    tstop = max(event_times[-1], epoch_times[-1], st_times[-1]) + 1 * pq.ms
    st = SpikeTrain(name="Seg {} :: SpikeTrain".format(idx),
                    times=st_times, t_start=tstart, t_stop=tstop)
    wf = np.random.random((len(st_times), nchannels, 30)) * pq.mV
    st.waveforms = wf
    st.sampling_rate = sampling_rate

    seg.spiketrains.append(st)

    unit = Unit(name="unit-{}".format(idx))
    unit.spiketrains.append(st)
    print(chx.name)
    chx.units.append(unit)

# Write the Block to file using the NixIO
# Any existing file will be overwritten
fname = "neoraw.nix"
io = NixIO(fname, "ow")
io.write_block(block)
io.close()

print("Done. Saved to {}".format(fname))
