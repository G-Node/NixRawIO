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
        print(filename)

    def _source_name(self):
        return self.filename

    def _parse_header(self):  # at Least no errors while running

        # alldas = [da for da in bl.data_arrays for bl in file.blocks]
        # alldasrc = [dasrc for dasrc in da.sources for da in bl.data_arrays for bl in file.blocks]
        self.file = nix.File.open(self.filename, nix.FileMode.ReadOnly)
        sig_channels = []
        sig_info = []
        ch_name = ""
        chan_id = ""
        for bl in self.file.blocks:
            # print("\t\t block: {}".format(bl))
            for src in bl.sources:
                if src.type == "neo.channelindex":
                    # print("\t\t src.type: {}".format(src.type))
                    for csrc in src.sources:
                        if csrc.type != "neo.channelindex":
                            # print("\t\t csrc.type: {}".format(csrc.type))
                            continue
                        ch_name = csrc.metadata["neo_name"]
                        # print("\t\t ch_name: {}".format(ch_name))
                        chan_id = csrc.metadata["channel_id"]  # refer to notes 1 to find the exact metadata mapping
                        # print("\t\t name: {}".format(chan_id))
            for da in bl.data_arrays:
                for dsrc in da.sources:
                    if dsrc.type == "neo.channelindex":
                        units = da.unit
                        # print("\t\t units: {}".format(units))
                        dtype = da.dtype
                        # print("\t\t dtype: {}".format(dtype))
                        sr = 0
                        if da.type == "neo.analogsignal":
                            sr = 1 / da.dimensions[0].sampling_interval
                            # print("\t\t sr: {}".format(sr))
                        group_id = 0
                        # print("\t\t group_id: {}".format(group_id))
                        gain = 1
                        offset = 0.
                        sig_channels.append((ch_name, chan_id, sr, dtype, units, gain, offset, group_id))
        sig_channels = np.array(sig_channels, dtype=_signal_channel_dtype)
        # print("\t\t sig_channel: {}".format(sig_channels))

        unit_channels = []
        unit_name = ""
        unit_id = ""
        for bl in self.file.blocks:
            # print("\t\t u_block: {}".format(bl))
            for mt in bl.multi_tags:
                if mt.type == "neo.spiketrain":
                    for usrc in mt.sources:
                        if usrc.type == "neo.unit":
                            unit_name = usrc.name
                            # print("\t\t unit_name: {}".format(unit_name))
                            unit_id = usrc.id
                            # print("\t\t unit_id: {}".format(unit_id))
                            pass
            for da in bl.data_arrays:
                if da.type == "neo.waveforms":
                    wf_units = da.unit
                    wf_gain = 0
                    wf_offset = 0.
                    # print("\t\t :wf_offset {}".format(wf_offset))
                    wf_left_sweep = 10
                    wf_sampling_rate = 1/da.dimensions[2].sampling_interval
                    unit_channels.append((unit_name, unit_id, wf_units, wf_gain,
                                          wf_offset, wf_left_sweep, wf_sampling_rate))
        unit_channels = np.array(unit_channels, dtype=_unit_channel_dtype)
        # print("\t\t unit_channels: {}".format(unit_channels))

        event_channels = []
        event_count = 0
        epoch_count = 0
        for bl in self.file.blocks:
            for mt in bl.multi_tags:
                if mt.type == "neo.event":
                    ev_name = mt.name
                    # print("\t\t ev_name: {}".format(ev_name))
                    ev_id = event_count
                    event_count += 1
                    ev_type = "event"
                    event_channels.append((ev_name, ev_id, ev_type))
                if mt.type == "neo.epoch":
                    ep_name = mt.name
                    ep_id = epoch_count
                    epoch_count += 1
                    ep_type = "epoch"
                    event_channels.append((ep_name, ep_id, ep_type))
        event_channels = np.array(event_channels, dtype=_event_channel_dtype)
        # print("\t\t event_channels: {}".format(event_channels))

        self.header = {}
        self.header['nb_block'] = len(self.file.blocks)
        self.header['nb_segment'] = [len(bl.groups) for bl in self.file.blocks]
        self.header['signal_channels'] = sig_channels
        self.header['unit_channels'] = unit_channels
        self.header['event_channels'] = event_channels

        self._generate_minimal_annotations()

        ac = 0  # cannot integrate into for loop because objects are not iterable
        stc = 0
        ec = 0

        for block_index in range(len(self.file.blocks)):
            bl_ann = self.raw_annotations['blocks'][block_index]
            # print("\t\t bl_ann: {}".format(bl_ann))
            seg_range = [len(bl.groups) for bl in self.file.blocks]
            for seg_index in range(seg_range[block_index]):
                seg_ann = bl_ann['segments'][seg_index]
                for da in self.file.blocks[block_index].data_arrays:
                    if da.type == "neo.analogsignal":
                        anasig_an = seg_ann['signals'][ac]  # should I include irregular signals?
                        ac += 1
                for st in unit_channels:
                    spiketrain_an = seg_ann['units'][stc]
                    # print("\t\t spiketrain_an: {}".format(spiketrain_an))
                    stc += 1
                for e in event_channels:
                    even_an = seg_ann['events'][ec]
                    ec += 1

    def _segment_t_start(self, block_index, seg_index):  # Done!
        t_start = 0
        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
            if mt.type == "neo.spiketrain":
                t_start = mt.metadata['t_start']
        return t_start

    def _segment_t_stop(self, block_index, seg_index):  # Done!
        t_stop = 0
        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
            if mt.type == "neo.spiketrain":
                t_stop = mt.metadata['t_stop']
        return t_stop

    def _get_signal_size(self, block_index, seg_index, channel_indexes):   # Done!
        size = 0
        for da in self.file.blocks[block_index].data_arrays:
            if da.type == 'neo.analogsignal':
                size = da.size
        return size

    def _get_signal_t_start(self, block_index, seg_index, channel_indexes):  # Done!
        sig_t_start = 0
        for bl in self.file.blocks:
            for da in bl.data_arrays:
                if da.type == 'neo.analogsignal':
                    sig_t_start = float(da.metadata['t_start'])
        return sig_t_start

    def _get_analogsignal_chunk(self, block_index, seg_index, i_start, i_stop, channel_indexes):  # Done!
        if i_start is None:
            i_start = 0
        if i_stop is None:
            i_stop = min(len(da) for da in self.file.blocks[block_index].data_arrays if da.type == "neo.analogsignal")
        if channel_indexes is None:
            chan_list = []
            for chan in self.file.blocks[block_index].sources:
                if chan.type == "neo.channelindex":
                    chan_list.append(chan)

            nb_chan = chan_list
        else:
            nb_chan = channel_indexes

        raw_signals_list = []
        for ch in self.file.blocks[block_index].sources:
            for csrc in ch.sources:
                if csrc.type == "neo.channelindex" and csrc.metadata["channel_id"] in nb_chan:  # returning the same sequence regardless of the channel_index
                    # print(csrc) 6 channel_indexes and one unit type= neo.unit
                    # try:
                        # if csrc.metadata["channel_id"] in nb_chan: # should I use any or all?
                            # print(i_start, i_stop)  # even i start i stop change, returned array unchange
                    for da in self.file.blocks[block_index].groups[seg_index].data_arrays:
                        if da.type == "neo.analogsignal" and ch in da.sources:
                            print("Adding", da.metadata["neo_name"], da.name)
                            raw_signals_list.append(da[i_start:i_stop])
                        else:
                            print("Skip", da.metadata["neo_name"])
                else:
                    print("Skipping", csrc.metadata["neo_name"])

                            # print(np.shape(da), da.name)  # maybe I should use
                    # except KeyError:
                        # pass
        raw_signals = np.array(raw_signals_list) # test asserted ndmin should be 2
        # length of da always different / raise value error
        print(np.shape(raw_signals))
        return raw_signals

    def _spike_count(self, block_index, seg_index, unit_index):         # Done!
        count = 0
        for bl in self.file.blocks:
            for mt in bl.multi_tags:
                if mt.type == 'neo.spiketrain':
                    count += 1
        return count

    def _get_spike_timestamps(self, block_index, seg_index, unit_index, t_start, t_stop):  # Done!
        spike_timestamps = []
        for mt in self.file.blocks[block_index].multi_tags:
            if mt.type == 'neo.spiketrain':
                st_times = mt.positions
                spike_timestamps.append(st_times)
        spike_timestamps = np.array(spike_timestamps)

        if t_start is not None or t_stop is not None:  # assumed t_start and T-stop unit is S
            lim0 = t_start
            lim1 = t_stop
            mask = (spike_timestamps >= lim0) & (spike_timestamps <= lim1)
            spike_timestamps = spike_timestamps[mask]
        return spike_timestamps

    def _rescale_spike_timestamp(self, spike_timestamps, dtype):  # Done!
        spike_times = spike_timestamps.astype(dtype)
        sr = 0
        # TODO: sr = self.header['signal_channels'][]
        for bl in self.file.blocks:
            for da in bl.data_arrays:
                if da.type == "neo.analogsignal":
                    for di in da.dimensions:
                        sr = 1 / di.sampling_interval
        spike_times *= sr
            # nix use sampl interval instead of sr
            # sr = 1 / da.dimensions[0].sampling_interval
        return spike_times

    def _get_spike_raw_waveforms(self, block_index, seg_index, unit_index, t_start, t_stop):  # Done!
        # this must return a 3D numpy array (nb_spike, nb_channel, nb_sample)
        waveforms = []
        for da in self.file.blocks[block_index].groups[seg_index].data_arrays:
            if da.type == "neo.waveforms":
                waveforms.append(da)
        if self.file.blocks[block_index].groups[seg_index].multi_tags.type == "neo.spiketrains":
            nb_spike = enumerate(self.file.blocks[block_index].groups[seg_index].multi_tags) # add if neo spiketrain
        nb_channel = enumerate(self.file.blocks[block_index].groups[seg_index].multi_tags)
        nb_sample = 0  # what is sample?
        raw_waveforms = np.array(waveforms)
        raw_waveforms.reshape(nb_spike, nb_channel, nb_sample)
        return raw_waveforms

    def _event_count(self, block_index, seg_index, event_channel_index):  # Done!
        event_count = 0
        for bl in self.file.blocks:
            for event in bl.multi_tags:
                if event.type == 'neo.event':
                    event_count += 1
        return event_count

    def _get_event_timestamps(self, block_index, seg_index, event_channel_index, t_start, t_stop):  # Done!
        seg_t_start = self._segment_t_start(block_index, seg_index)
        timestamp = []
        labels = []

        for mt in self.file.blocks[block_index].multi_tags:
            if mt.type == "neo.event":
                labels.append(mt.positions.dimensions[0].labels)
                po = mt.positions
                if po.type == "neo.event.times":
                    timestamp.append(po)
        timestamp = np.array(timestamp, dtype="float") + seg_t_start
        # print("\t\t ev_timestamp: {}".format(timestamp))
        labels = np.array(labels, dtype='U')
        # print("\t\t ev_labels: {}".format(labels))

        if t_start is not None:
            keep = timestamp >= t_start
            timestamp, labels = timestamp[keep], labels[keep]

        if t_stop is not None:
            keep = timestamp <= t_stop
            timestamp, labels = timestamp[keep], labels[keep]
        durations = None
        return timestamp, durations, labels

    def _rescale_event_timestamp(self, event_timestamps, dtype):  # Done!
        event_times = event_timestamps.astype(dtype)  # supposing unit is second, other possibilies maybe mS microS...
        return event_times

    def _rescale_epoch_duration(self, raw_duration, dtype):  # Done!
        durations = raw_duration.astype(dtype)  # supposing unit is second, other possibilies maybe mS microS...
        return durations
