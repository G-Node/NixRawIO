from __future__ import print_function, division, absolute_import
from neo.rawio.baserawio import (BaseRawIO, _signal_channel_dtype, _unit_channel_dtype,_event_channel_dtype)
import numpy as np
from collections import OrderedDict
import quantities
import neo
import urllib.request
import nixio as nix

filename = 'example-file.nix'
file = nix.File.open(filename, nix.FileMode.ReadOnly)


nb_block = len(file.blocks)
print(nb_block)

def read_as_dict(file, dtype, offset=None):
    """
    Given a file descriptor
    and a numpy.dtype of the binary struct return a dict.
    Make conversion for strings.
    """
    if offset is not None:
        file.seek(offset)
    dt = np.dtype(dtype)
    h = np.fromstring(file.read(dt.itemsize), dt)[0]
    info = OrderedDict()
    for k in dt.names:
        v = h[k]

        if dt[k].kind == 'S':
            v = v.decode('utf8')
            v = v.replace('\x03', '')
            v = v.replace('\x00', '')

        info[k] = v
    return info


GlobalHeader = [
    ('ID', 'int64')
]
with io.open(self.filename, 'rb') as f:
    sig_channels = []
    for c in enumerate():
        dtype = 'int16'
        sig_channels.append((dtype))
    sig_channels = np.array(sig_channels, dtype=_signal_channel_dtype)

    unit_channels = []

    event_channels = []
    if (file.blocks.multi_tags.type == 'neo.event'):
        event_channels.append(file.blocks.multi_tags.id, 'event')
    if (file.blocks.multi_tags.type == 'neo.epoch'):
        event_channels.append(file.blocks.multi_tags.id, 'epoch')
    event_channels = np.array(event_channels, dtype=_event_channel_dtype)

    self.header = {}

    self._generate_minimal_annotations()

'''


        self._data_blocks = {}
        dt_base = [('pos', 'int64'), ('timestamp', 'int64'), ('size', 'int64')]
        dtype_by_bltype = {

            1: np.dtype(dt_base + [('unit_id', 'uint16'), ('n1', 'uint16'), ('n2', 'uint16'), ]),

            4: np.dtype(dt_base + [('label', 'uint16'), ]),

            5: np.dtype(dt_base + [('cumsum', 'int64'), ]),
        }



        self.internal_unit_ids = []
        try:
            for chan_id, data_clock in self._data_blocks[1].items():

                unit_ids = np.unique(data_clock['unit_id'])
        except KeyError:
            unit_ids = np.unique(data_clock['unit_id'])
            for unit_id in unit_ids:
                self.internal_unit_ids.append((chan_id, unit_id))

    def _get_spike_timestamps(self, block_index, seg_index, unit_index, t_start, t_stop):
        chan_id, unit_id = self.internal_unit_ids[unit_index]
        data_block = self._data_blocks[1][chan_id]

        keep = self._get_internal_mask(data_block, t_start, t_stop)
        keep &= data_block['unit_id'] == unit_id
        spike_timestamps = data_block[keep]['timestamp']

        return spike_timestamps

    def _rescale_spike_timestamp(self, spike_timestamps, dtype):
        spike_times = spike_timestamps.astype(dtype)
        spike_times /= self._global_ssampling_rate


        return spike_times

    def _get_internal_mask(self, data_block, t_start, t_stop):
        timestamps = data_block['timestamp']

        if t_start is None:
            lim0 = 0
        else:
            lim0 = int(t_start * self._global_ssampling_rate)

        if t_stop is None:
            lim1 = self._last_timestamps
        else:
            lim1 = int(t_stop * self._global_ssampling_rate)

        keep = (timestamps >= lim0) & (timestamps <= lim1)

        return keep


'''

def read_nix(file):
    rawio = NixRawIO._parse_header(file)
    info = {}
    return info

filename = 'NeoMapping.nix'
file = nix.File.open(filename, nix.FileMode.ReadOnly)

if da.type == "neo.irregularlysampledsignal":  # da.source.type or da.type is fine?
    iranasig_an = seg_ann['signals'][ac]
    ac += 1