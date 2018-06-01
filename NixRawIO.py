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

    def _parse_header(self):

        self.file = nix.File.open(self.filename, nix.FileMode.ReadOnly)
        channel_name = []
        for blk in self.file.blocks:
            for ch, src in enumerate(blk.sources):
                channel_name.append(src.name)

        sig_channels = []
        for bl in self.file.blocks:
            didx = 0
            for da in bl.data_arrays:
                if da.type == "neo.analogsignal":
                    # print(didx, da)
                    # for dsrc in da.sources: # channelindex
                        # ch_name = dsrc.metadata["neo_name"] or dsrc.sources.metadata... ?
                        # for csrc in dsrc.sources: # channelindex children/ unit
                            # if csrc.type == "neo.channelindex
                    #chan_id = str(da.metadata["neo_name"][-1]) +str(didx)
                    nixname = da.name
                    nixidx = int(nixname.split('.')[-1])
                    src = da.sources[0].sources[nixidx]
                    chan_id = src.metadata['channel_id']
                    ch_name = src.metadata['neo_name']
                    #print("id is", chan_id, "name is", ch_name)
                    #print('-------------')
                    # print(da.sources[0].sources[didx].metadata['channel_id'])
                    # print(da.sources[0].sources[didx].metadata['neo_name'])
                    units = str(da.unit)
                    dtype = str(da.dtype)
                    sr = 1 / da.dimensions[0].sampling_interval
                    group_id = 0
                    for id, name in enumerate(channel_name):
                        if name == da.sources[0].name:
                            group_id = id
                    gain = 1
                    offset = 0.
                    sig_channels.append((ch_name, chan_id, sr, dtype, units, gain, offset, group_id))
                    didx += 1
        sig_channels = np.array(sig_channels, dtype=_signal_channel_dtype)
        # print("\t\t sig_channel: {}".format(sig_channels))

        unit_channels = []
        unit_name = ""
        unit_id = ""
        for bl in self.file.blocks:
            # print("\t\t u_block: {}".format(bl))
            for seg in bl.groups:
                for mt in seg.multi_tags:
                    if mt.type == "neo.spiketrain":
                        for usrc in mt.sources:
                            if usrc.type == "neo.unit":
                                unit_name = usrc.name
                                # print("\t\t unit_name: {}".format(unit_name))
                                unit_id = usrc.id
                                # print(unit_id)
                                pass
                        wf_units = mt.features[0].data.unit
                        wf_gain = 0
                        wf_offset = 0.
                        if "left_sweep" in mt.features[0].data.metadata:
                            wf_left_sweep = mt.features[0].data.metadata["left_sweep"]  # what is left sweep
                        else:
                            wf_left_sweep = 0
                        wf_sampling_rate = 1 / mt.features[0].data.dimensions[2].sampling_interval
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
        if channel_indexes is None:
            channel_indexes = []
        for ch in channel_indexes:
            ch = int(ch)
            chan_name = self.file.blocks[block_index].sources[ch].name
            for da in self.file.blocks[block_index].groups[seg_index].data_arrays:
                if da.type == 'neo.analogsignal' and da.sources[0].name == chan_name:
                    size += da.size
        return size

    def _get_signal_t_start(self, block_index, seg_index, channel_indexes):  # Done!
        sig_t_start = 0
        if channel_indexes is None:
            channel_indexes = []
        for ch in channel_indexes:
            ch = int(ch)
            chan_name = self.file.blocks[block_index].sources[ch].name
            for da in self.file.blocks[block_index].groups[seg_index].data_arrays:
                if da.type == 'neo.analogsignal' and da.sources[0].name == chan_name:
                    sig_t_start = float(da.metadata['t_start'])
                    break
        return sig_t_start

    def _get_analogsignal_chunk(self, block_index, seg_index, i_start, i_stop, channel_indexes):  # chan must be list!
        if i_start is None:
            i_start = 0
        if i_stop is None:
            i_stop = min(len(da) for da in self.file.blocks[block_index].groups[seg_index].data_arrays
                         if da.type == 'neo.analogsignal')
        chan_list = []
        for chan in self.file.blocks[block_index].sources:
            if chan.type == "neo.channelindex":
                chan_list.append(chan)
        if channel_indexes is None:
            for i, data in enumerate(chan_list):
                nb_chan = []
                nb_chan.append(i)
        else:
            keep =[]
            for ch in channel_indexes:
                keep.append(ch <= len(chan_list) - 1)
            nb_chan = [i for (i, v) in zip(channel_indexes, keep) if v]

        raw_signals_list = []
        for ch in nb_chan:
            ch = int(ch)
            chan_name = self.file.blocks[block_index].sources[ch].name
            for da in self.file.blocks[block_index].groups[seg_index].data_arrays:
                if da.type == 'neo.analogsignal' and da.sources[0].name == chan_name:
                    raw_signals_list.append(da[i_start:i_stop])
                #else:
                    #print("Skip", da.metadata["neo_name"])
        raw_signals = np.array(raw_signals_list)
        raw_signals = np.transpose(raw_signals)
        #sig_name = self.header['signal_channels'][2][1]
        #print(sig_name)
        #print(self.file.blocks[block_index].groups[seg_index].data_arrays)
        #print(raw_signals.shape)
        #print(np.shape(raw_signals))
        #print(raw_signals)
        return raw_signals

    def _spike_count(self, block_index, seg_index, unit_index):         # Done!
        count = 0
        head_id = self.header['unit_channels'][unit_index][1]
        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
            for src in mt.sources:
                if mt.type == 'neo.spiketrain' and [src.type == "neo.unit"]:
                    if head_id == src.id:
                        count += 1
        return count

    def _get_spike_timestamps(self, block_index, seg_index, unit_index, t_start, t_stop):  # Done!
        spike_timestamps = []
        head_id = self.header['unit_channels'][unit_index][1]  # not going to work unit_index can be list or array
        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
            for src in mt.sources:
                if mt.type == 'neo.spiketrain' and [src.type == "neo.unit"]:
                    if head_id == src.id:
                        st_times = mt.positions
                        spike_timestamps.append(st_times)
        spike_timestamps = np.array(spike_timestamps)

        if t_start is not None or t_stop is not None:
            lim0 = t_start
            lim1 = t_stop
            mask = (spike_timestamps >= lim0) & (spike_timestamps <= lim1)
            spike_timestamps = spike_timestamps[mask]
        return spike_timestamps

    def _rescale_spike_timestamp(self, spike_timestamps, dtype):  # Done!
        spike_times = spike_timestamps.astype(dtype)
        sr= self.header['signal_channels'][0][2]
        spike_times *= sr
            # nix use sampl interval instead of sr
            # sr = 1 / da.dimensions[0].sampling_interval
        return spike_times

    def _get_spike_raw_waveforms(self, block_index, seg_index, unit_index, t_start, t_stop):
        # this must return a 3D numpy array (nb_spike, nb_channel, nb_sample)
        waveforms = []
        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
            if mt.type == "neo.spiketrain":
                if mt.features[0].data.type == "neo.waveforms":
                    waveforms.append(mt.features[0].data)
        raw_waveforms = np.array(waveforms)
        rs = raw_waveforms.shape

        raw_waveforms.reshape(rs[1], rs[2], rs[3])
        if t_start is not None or t_stop is not None:
            lim0 = t_start
            lim1 = t_stop
            mask = (raw_waveforms >= lim0) & (raw_waveforms <= lim1)
            raw_waveforms = raw_waveforms[mask]
        return raw_waveforms

    def _event_count(self, block_index, seg_index, event_channel_index):  # Done!
        event_count = 0
        for event in self.file.blocks[block_index].groups[seg_index].multi_tags:
            if event.type == 'neo.event':
                event_count += 1
        return event_count

    def _get_event_timestamps(self, block_index, seg_index, event_channel_index, t_start, t_stop):  # Done!
        seg_t_start = self._segment_t_start(block_index, seg_index)
        timestamp = []
        labels = []

        for mt in self.file.blocks[block_index].groups[seg_index].multi_tags:
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

