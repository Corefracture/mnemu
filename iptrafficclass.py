import netem_defs as nems


class NetemSettings:
    def __init__(self):
        self.loss = nems.NetemLoss()
        self.dupe = nems.NetemDupe()
        self.reorder = nems.NetemReorder()
        self.corrupt = nems.NetemCorrupt()
        self.latency = nems.NetemLatency()

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.loss,
                                            self.dupe,
                                            self.reorder,
                                            self.corrupt,
                                            self.latency)


class IPTrafficClass:

    def __init__(self, ip, in_id, out_id, parent_id):
        self.ip = ip
        self.in_id = in_id
        self.out_id = out_id
        self.parent_id = parent_id
        self.stage_changed_ms = 0
        self.in_rate = '10024'
        self.out_rate = '10024'

        self.in_netem = NetemSettings()
        self.out_netem = NetemSettings()

        self.script_id = None
        self.script_stage_id = None

    def set_script_id(self, script_id):
        self.script_id = script_id

    def set_script_stage(self, script_stage_id):
        self.script_stage_id = script_stage_id

    def get_last_stage_change_ms(self):
        return self.stage_changed_ms
