from __future__ import print_function, division, absolute_import
from neo.rawio.baserawio import (BaseRawIO, _signal_channel_dtype, _unit_channel_dtype, _event_channel_dtype)
import numpy as np
import nixio as nix


class NixRawIO (BaseRawIO):

    extensions = ['nix']
    rawmode = 'one-file'

    def __init__(self, filename=''):
        BaseRawIO.__init__(self)
        self.filename = filename

    def _source_name(self):
        return self.filename

    def _parse_header(self):

        # alldas = [da for da in bl.data_arrays for bl in file.blocks]
        # alldasrc = [dasrc for dasrc in da.sources for da in bl.data_arrays for bl in file.blocks]
        self.file = nix.File.open(self.filename, nix.FileMode.ReadOnly)
        sig_channels = []
        ch_name = ""
        chan_id = ""
        for bl in self.file.blocks:
            print("\t\t block: {}".format(bl))
            for src in bl.sources:
                if src.type == "neo.channelindex":
                    print("\t" + src.type)
                    for csrc in src.sources:
                        if csrc.type != "neo.channelindex":
                            print("\t\t csrc.type: {}".format(csrc.type))
                            continue
                        ch_name = csrc.metadata["neo_name"]
                        print("\t\t ch_name: {}".format(ch_name))
                        chan_id = csrc.metadata["channel_id"]  # refer to notes 1 to find the exact metadata mapping
                        print("\t\t name: {}".format(chan_id))
            for da in bl.data_arrays:
                for dsrc in da.sources:
                    if dsrc.type == "neo.channelindex":
                        units = da.unit
                        print("\t\t units: {}".format(units))
                        dtype = da.dtype
                        print("\t\t dtype: {}".format(dtype))
                        sr = 0
                        if da.type == "neo.analogsignal":
                            sr = 1 / da.dimensions[0].sampling_interval
                            print("\t\t sr: {}".format(sr))
                        group_id = 0
                        print("\t\t group_id: {}".format(group_id))
                        gain = 1
                        offset = 0.
                        sig_channels.append((ch_name, chan_id, sr, dtype, units, gain, offset, group_id))
        sig_channels = np.array(sig_channels, dtype=_signal_channel_dtype)
        print("\t\t sig_channel: {}".format(sig_channels))

        unit_channels = []
        unit_name = ""
        unit_id = ""
        for bl in self.file.blocks:
            print("\t\t block: {}".format(bl))
            for usrc in bl.sources:
                if usrc.type == "neo.unit":
                    unit_name = usrc.name
                    print("\t\t unit_name: {}".format(unit_name))
                    unit_id = usrc.id
                    print("\t\t unit_id: {}".format(unit_id))
            for mt in bl.multi_tags:
                for msrc in mt.sources:
                    if msrc.type == "neo.spiketrain":
                        wf_units = "mV"   # this is assuming wf= None, should be change
                        wf_gain = 0
                        wf_offset = 0.
                        wf_left_sweep = 10
                        wf_sampling_rate = 1000.
                        unit_channels.append((unit_name, unit_id, wf_units, wf_gain,
                                              wf_offset, wf_left_sweep, wf_sampling_rate))
        unit_channels = np.array(unit_channels, dtype=_unit_channel_dtype)
        print("\t\t unit_channels: {}".format(unit_channels))

        event_channels = []
        for bl in self.file.blocks:
            for mt in bl.multi_tags:
                for msrc in mt.sources:
                    event_count = 0
                    epoch_count = 0
                    if msrc.type == "neo.event":
                        ev_name = mt.name
                        ev_id = event_count
                        event_count += 1
                        ev_type = "event"
                        event_channels.append(ev_name, ev_id, ev_type)
                    if msrc.type == "neo.epoch":
                        ep_name = mt.name
                        ep_id = epoch_count
                        epoch_count += 1
                        ep_type = "epoch"
                        event_channels.append(ep_name, ep_id, ep_type)
        event_channels = np.array(event_channels, dtype=_event_channel_dtype)
        print("\t\t event_channels: {}".format(event_channels))

        self.header = {}
        self.header['nb_block'] = len(self.file.blocks)
        self.header['nb_segment'] = [len(bl.groups) for bl in self.file.blocks]
        self.header['signal_channels'] = sig_channels
        self.header['unit_channels'] = unit_channels
        self.header['event_channels'] = event_channels

        self._generate_minimal_annotations()

        for bl in self.file.blocks:
            for block_index in range(len(self.file.blocks)):
                bl_ann = self.raw_annotations['blocks'][block_index]
                print("\t\t bl_ann: {}".format(bl_ann))
            for seg in bl.groups:
                seg_index = 0
                seg_ann = bl_ann['segments'][seg_index]
                seg_index += 1
                for da in self.file.blocks[block_index].data_arrays:
                    if da.type == "neo.analogsignal":
                        anasig_an = seg_ann['signals'][da]
                    if da.type == "neo.irregularlysampledsignal":  # da.source.type or da.type is fine?
                        iranasig_an = seg_ann['signals'][da]
                for st in unit_channels:
                    spiketrain_an = seg_ann['units'][st]
                for e in event_channels:
                    even_an = seg_ann['events'][e]

    def _segment_t_start(self, block_index, seg_index):  # how to do multitags indexing
        t_start = 0
        for gp in self.file.blocks[block_index].groups:
            for da in gp.data_arrays:
                if da.type == "neo.analogsignal":
                    t_start = da.metadata['t_start']  # should be groups or multitag?
        return t_start

    def _segment_t_stop(self, block_index, seg_index):
        t_stop = self.file.blocks[block_index].multi_tags.metadata['t_stop']
        return t_stop

    def _get_signal_size(self, block_index, seg_index, channel_indexes):   # Done!
        size = 0
        for da in self.file.blocks[block_index].data_arrays:
            if da.type == 'neo.analogsignal':
                size = da.size
        return size

    def _get_signal_t_start(self, block_index, seg_index, channel_indexes):
        sig_t_start = 0
        for bl in self.file.blocks:
            for da in bl.data_arrays:
                for src in da.sources:
                    if src.type == 'neo.analogsignal':
                        sig_t_start = float(da.metadata['t_start'])
        return sig_t_start

    def _get_analogsignal_chunk(self, block_index, seg_index, i_start, i_stop, channel_indexes):  # Done!
        if i_start is None:
            i_start = 0
        if i_stop is None:
            i_stop = len(self.file.groups.data_arays)
        if channel_indexes is None:
            chan_list = []
            for chan in self.file.blocks[block_index].source.type == "neo.channelindex":
                # not sure if I understand the parameter right
                chan_list.append(chan)
            nb_chan = chan_list  # should be None or list or np.array
        else:
            nb_chan = channel_indexes  # should there be sth checking if the type is channelindex

        raw_signals_list = []
        for ch in self.file.blocks[block_index].sources:
            for csrc in ch.sources:
                if csrc.type == "neo.channelindex":
                    if csrc.metadata["channel_id"] == nb_chan:
                        for i in range(i_start, i_stop):
                            for da in self.file.blocks[block_index].data_arrays[i]:
                                raw_signals_list.append(da)
        raw_signals = np.array(raw_signals_list)
        return raw_signals

    def _spike_count(self, block_index, seg_index, unit_index):         # Done!
        count = 0
        for bl in self.file.blocks:
            for mt in bl.multi_tags:
                if mt.type == 'neo.spiketrain':
                    count += 1
        return count

    def _get_spike_timestamps(self, block_index, seg_index, unit_index, t_start, t_stop):

        if self.file.blocks.multi_tags.sources.type == 'neo.spiketrain':
            spike_timestamps = self.file.blocks.multi_tags.metadata['t_stop'] - self.file.blocks.multi_tags.metadata['t_start']
        else:
            return None
        if t_start is not None or t_stop is not None:
            lim0 = int(t_start)
            lim1 = int(t_stop)
            mask = (spike_timestamps >= lim0) & (spike_timestamps <= lim1)
            spike_timestamps = spike_timestamps[mask]
        return spike_timestamps

    def _rescale_spike_timestamp(self, spike_timestamps, dtype):
        spike_times = spike_timestamps.astype(dtype)
        if self.file.blocks.data_arrays.type == "neo.spiketrain":
            spike_times *= self.file.blocks.data_arrays.dimensions["SampledDimension"]
            # nix use sampl interval instead of sr
            # sr = 1 / da.dimensions[0].sampling_interval
        return spike_times

    def _get_spike_raw_waveforms(self, block_index, seg_index, unit_index, t_start, t_stop):  # Done!
        return "there is no waveforms!"

    def _event_count(self, block_index, seg_index, event_channel_index):  # Done!
        event_count = 0
        for bl in self.file.blocks:
            for event in bl.multi_tags:
                if event.type == 'neo.event':
                    event_count += 1
        return event_count

    def _get_event_timestamps(self, block_index, seg_index, event_channel_index, t_start, t_stop):
        seg_t_start = self._segment_t_start(block_index, seg_index)
        timestamp = []
        labels = ""

        for mt in self.file.blocks[block_index].multi_tags:
            if mt.type == "neo.event":
                timestamp = np.array(3,3) + seg_t_start  # np array should be replaced by some attributes
                labels = mt.name  # not sure if correct

        if t_start is not None:
            keep = timestamp >= t_start
            timestamp, labels = timestamp[keep], labels[keep]

        if t_stop is not None:
            keep = timestamp <= t_stop
            timestamp, labels = timestamp[keep], labels[keep]
        durations = None
        return timestamp, durations, labels

    def _rescale_event_timestamp(self, event_timestamps, dtype):
        event_times = event_timestamps.astype(dtype)  # supposing unit is second, other possibilies maybe mS microS...
        return event_times

    def _rescale_epoch_duration(self, raw_duration, dtype):
        durations = raw_duration.astype(dtype)  # supposing unit is second, other possibilies maybe mS microS...
        return durations





