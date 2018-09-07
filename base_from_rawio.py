from neo.io.basefromrawio import BaseFromRaw
from nixrawio import NixRawIO
import nixio as nix
import numpy as np
import unittest
import os
from nixio_fr import NixIOfr
import quantities as pq


class TestNixfr(unittest.TestCase):

    def setUp(self):
        self.testfilename = "test_case.nix"
        self.file = nix.File.open(self.testfilename, nix.FileMode.ReadOnly)
        self.reader = NixIOfr(filename=self.testfilename)
        self.blk = self.reader.read_block(0, load_waveforms= True)
        self.blk1 = self.reader.read_block(1, load_waveforms= True)

    def tearDown(self):
        self.file.close()

    def test_analog_signal(self):
        seg1 = self.blk.segments[0]
        an_sig1 = seg1.analogsignals[0]
        assert len(an_sig1) == 30

        an_sig2 = seg1.analogsignals[1]
        list_c = an_sig2.tolist()
        assert an_sig2.shape == (50,3)

        an_sig3 = self.blk.segments[1].analogsignals[1]
        list_a = an_sig3.tolist()
        an_sig4 = self.blk1.segments[1].analogsignals[1]
        list_b = an_sig4.tolist()

        assert list_a == list_b == list_c

    def test_spiketrain(self):
        unit1 = self.blk.channel_indexes[3].units[0]
        st1 = unit1.spiketrains[0]
        print(st1.times)
        print(np.cumsum(np.arange(0,1,0.1)).tolist() * pq.ms + 10 *pq.ms)
        assert np.all(st1.times == np.cumsum(np.arange(0,1,0.1)).tolist() * pq.ms + 10 *pq.ms)

    def test_event(self):
        seg1 = self.blk.segments[0]
        event1 = seg1.events[0]
        assert np.all(event1.times == 10 * pq.ms + np.cumsum(np.array([0,1,2,3,4])) * pq.ms)

        assert np.all(event1.labels == np.array([b'A', b'B', b'C', b'D', b'E']))
        assert len(seg1.events) == 1

    def test_epoch(self):
        seg1 = self.blk.segments[1]
        epoch1 = seg1.epochs[0]

    def test_waveform(self):
        pass


localfile = '/home/choi/PycharmProjects/Nixneo/test_case.nix'

reader = NixIOfr(filename=localfile)
blk = reader.read_block(0, load_waveforms= True)
blk1 = reader.read_block(1, load_waveforms= True)
# print(blk)
# print(blk1)
# print(blk.name)
# print('//////////////////////////////////////////////////')
# print(blk.segments)

# for asig in blk.segments[0].analogsignals:
#     print("asigname", asig.name)
#     print(asig.shape)
# print(blk.segments[0].analogsignals[2])
# for asig in blk1.segments[0].analogsignals:
#     print("asigname with block 2", asig.name)
#     print(asig.shape)
# print('------------------------------------------------')
# for chx in blk.channel_indexes:
#      print(chx.name)
#      print(chx.channel_ids)
#      print(chx.channel_names)
#      print("index: {}:".format(chx.index))
#      print ("===========================")
#      print(chx.units)
#      for i, u in enumerate(chx.units):
#          print(u.name)
#          print(u.spiketrains)
#          print(u.spiketrains[i].times)
#          print(u.spiketrains[0].t_start)
#          print(u.spiketrains[0].t_stop)
#          for st in u.spiketrains:
#              print(st.waveforms.units)
# print(blk.segments[0].events)
# print(blk.segments[0].events[0].labels.astype)
# print(blk.segments[0].events[0].times)
# print(blk.segments[0].epochs[0].name)
# print(blk.segments[0].spiketrains)
# print(blk.segments[1].spiketrains)

if __name__ == '__main__':
    unittest.main()

