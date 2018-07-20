from neo import (Block, Segment,
                 AnalogSignal, IrregularlySampledSignal,
                 Event, Epoch, SpikeTrain,
                 ChannelIndex, Unit)
from neo.io.nixio import NixIO

import numpy as np
import quantities as pq


for b in range(3):
    # Create a Block called example
    block = Block("example" + str(b), description="The root block for this example")

    # Create a Segment called seg-ex1 and attach it to the Block
    seg_a = Segment("seg-ex1", description="Segment one")
    block.segments.append(seg_a)

    # A second segment with an added comment
    # The comment is an "annotation"; any keyword argument can be used
    seg_b = Segment("seg-ex2", description="Segment two",
                    comment="Second recording set")
    block.segments.append(seg_b)

    # Generate 3 fake data signals using numpy's random function
    # The shapes of the arrays are arbitrary
    data_a = np.random.random((300, 10))
    data_b = np.random.random((1200, 3))
    data_c = np.random.random((8000, 5))

    # random sampling times for data_b
    data_b_t = np.cumsum(np.random.random(1200))

    # Create one AnalogSignal and one IrregularlySampledSignal
    asig_a = AnalogSignal(name="Data A", signal=data_a, units="mV",
                          sampling_rate=pq.Quantity(10, "Hz"))
    isig_a = IrregularlySampledSignal(name="Sampled data", signal=data_b,
                                      units="nA",
                                      times=data_b_t, time_units="ms")

    # Attach the signals to the first segment
    seg_a.analogsignals.append(asig_a)
    seg_a.irregularlysampledsignals.append(isig_a)

    # Create a second AnalogSignal and attach it to the second segment
    st_a = AnalogSignal(name="Data A", signal=data_c * pq.mV,
                          sampling_rate=20 * pq.Hz)
    seg_b.analogsignals.append(st_a)



# Write the Block to file using the NixIO
# Replace NixIO with any other IO to change storage format
io = NixIO("example-file.nix", mode = 'ow')
io.write_block(block)


io.close()