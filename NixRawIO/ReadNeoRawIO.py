for bl in self.file.blocks:  # Can do that due to there should only one unity per segment
    for seg in bl.groups:
        for mt in seg.multi_tags:
            if mt.type == "neo.spiketrain":
                for usrc in mt.sources:
                    if usrc.type == "neo.unit":
                        unit_name = usrc.metadata['neo_name']  # or should
                        print("\t\t unit_name: {}".format(unit_name))
                        unit_id = usrc.id
                        print("\t\t unit_id: {}".format(unit_id))
                        pass
    for da in bl.data_arrays:
        print(da.sources)
        if da.type == "neo.waveforms":

            if [mt.name for mt in bl.multi_tags] == da.name.replace('.waveforms', ""):
                wf_units = da.unit
                # print("\t\t :wf_units {}".format(wf_units))
                wf_gain = 0
                wf_offset = 0.
                # print("\t\t :wf_offset {}".format(wf_offset))
                if "left_sweep" in da.metadata:
                    wf_left_sweep = da.metadata["left_sweep"]  # what is left sweep
                else:
                    wf_left_sweep = 0
                # print("\t\t :wf_left_sweep {}".format(wf_left_sweep))
                wf_sampling_rate = 1 / da.dimensions[2].sampling_interval
                # print("\t\t :wf_sampling_rate {}".format(wf_sampling_rate))
                unit_channels.append((unit_name, unit_id, wf_units, wf_gain,
                                      wf_offset, wf_left_sweep, wf_sampling_rate))