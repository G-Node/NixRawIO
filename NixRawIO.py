from __future__ import print_function, division, absolute_import
from neo.rawio.baserawio import (BaseRawIO, _signal_channel_dtype, _unit_channel_dtype,_event_channel_dtype)
import numpy as np
import nixio as nix
import io

filename = 'NeoMapping.nix'
file = nix.File.open(filename, nix.FileMode.ReadOnly)

class NixRawIO (BaseRawIO):

    extensions = ['nix']
    rawmode = 'one-file'

    def __init__(self, filename = ''):
        BaseRawIO.__init__(self)
        self.filename = filename

    def _source_name(self):
        return self.filename

    def _parse_header(self):

        sig_channels = []
        for bl in file.blocks:
            print("\t\t block: {}".format(bl))
            for src in bl.sources:
                if src.type == "neo.channelindex":
                    print("\t" + src.type)
                    for csrc in src.sources:
                        ch_name = csrc.metadata["neo_name"]
                        print("\t\t ch_name: {}".format(ch_name))
                        chan_id = csrc.metadata["channel_id"]  #refer to notes 1 to find the exact metadata mapping
                        print("\t\t name: {}".format(chan_id))
            for da in bl.data_arrays:
                for dsrc in da.sources:
                    if dsrc.type == "neo.channelindex":
                        units = da.unit
                        print("\t\t units: {}".format(units))
                        dtype = da.dtype
                        print("\t\t dtype: {}".format(dtype))
                        sr = 1/ da.dimensions[0].sampling_interval
                        print("\t\t sr: {}".format(sr))
                        group_id = 0
                        print("\t\t group_id: {}".format(group_id))
                        gain = 1
                        offset = 0.
                        sig_channels.append((ch_name, chan_id, sr, dtype, units, gain, offset, group_id))
                        sig_channels = np.array(sig_channels, dtype=_signal_channel_dtype)
        print("\t\t sig_channel: {}".format(sig_channels))

        unit_channels = []
        for bl in file.blocks:
            print("\t\t block: {}".format(bl))
            for usrc in bl.sources:
                if usrc.type == "neo.unit":
                    unit_name = usrc.name
                    print("\t\t unit_name: {}".format(unit_name))
                    unit_id = usrc.definition
                    print("\t\t unit_id: {}".format(unit_id))
            for mt in bl.multi_tags:
                for msrc in mt.sources:
                    if msrc.type == "neo.spiketrain":
                        wf_units= "mV"
                        wf_gain= 0
                        wf_offset= 0.
                        wf_left_sweep= 10
                        wf_sampling_rate= 1000.
                        unit_channels.append((unit_name, unit_id, wf_units, wf_gain, wf_offset, wf_left_sweep, wf_sampling_rate))
                        unit_channels = np.array(unit_channels, dtype=_unit_channel_dtype)
        print("\t\t unit_channels: {}".format(unit_channels))

        event_channels = []
        for bl in file.blocks:
            for mt in bl.multi_tags:
                for msrc in mt.sources:
                    event_count = 0
                    epoch_count = 0
                    if msrc.type == "neo.event":
                        name = mt.name
                        id=event_count
                        event_count += 1
                        type = "event"
                    if msrc.type == "neo.epoch":
                        name = mt.name
                        id = epoch_count
                        epoch_count += 1
                        type = "epoch"
                    event_channels.append(name, id, type)
                    event_channels = np.array(event_channels, dtype=_event_channel_dtype)
        print("\t\t event_channels: {}".format(event_channels))

        self.header = {}
        self.header['nb_block'] = 1
        self.header['nb_segment'] = [1]
        self.header['signal_channels'] = sig_channels
        self.header['unit_channels'] = unit_channels
        self.header['event_channels'] = event_channels

        self._generate_minimal_annotations()

        for block_index in range(file._block_count()):
            bl_ann = self.raw_annotations['blocks'][block_index]
            for seg_index in file.blocks.groups:
                seg_ann=bl_ann['segments'][seg_index]
                for da in file.blocks.data_arrays:
                    if da.sources.type == "neo.analogsignal":
                        anasig_an = seg_ann['signals'][da]
                    if da.sources.type == "neo.irregularlysampledsignal":
                        iranasig_an = seg_ann['signals'][da]
                for st in unit_channels:
                    spiketrain_an = seg_ann['units'][st]
                for e in event_channels:
                    even_an = seg_ann['events'][e]

    def _segment_t_start(self, block_index, seg_index):
        return 0.

    def _segment_t_stop(self, block_index, seg_index):
        t_stop =
        return

    def _get_signal_size(self, block_index, seg_index, channel_indexes):

    def _get_signal_t_start(self, block_index, seg_index, channel_indexes):

    def _get_analogsignal_chunk(self, block_index, seg_index, i_start, i_stop, channel_indexes):
        if i_start == None:
            i_start = 0
        if i_stop == None:
            i_stop = file.groups.data_arays.len()
        if channel_indexes == None:
            nb_chan = len() #len(signal_channel)
        else:
            nb_chan = len(channel_indexes)
        raw_signals = np.zeros((i_stop - i_start, nb_chan), dtype='int16') #self.raw_signals? Q1
        return raw_signals
    def _spike_count(self, block_index, seg_index, unit_index):



def read_nix(file):
    NixRawIO._parse_header(file)
    info = {}
    return info
