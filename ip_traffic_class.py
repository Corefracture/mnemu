class netem_corrupt:
    def __init__(self, base_corrupt='0', correlation=None):
        self.base_corrupt = base_corrupt
        self.correlation = correlation

    def __str__(self):
        corrupt_str = 'corrupt' + self.base_corrupt
        if self.correlation is not None:
            corrupt_str = corrupt_str + " " + self.correlation + "%"

        return corrupt_str


class netem_reorder:
    def __init__(self, base_reorder='0', correlation=None):
        self.base_reorder = base_reorder
        self.correlation = correlation

    def __str__(self):
        reorder_str = 'reorder' + self.base_reorder
        if self.correlation is not None:
            reorder_str = reorder_str + " " + self.correlation + "%"

        return reorder_str


class netem_dupe:
    def __init__(self, base_dupe='0', correlation=None):
        self.base_dupe = base_dupe
        self.correlation = correlation

    def __str__(self):
        dupe_str = 'duplicate' + self.base_dupe
        if self.correlation is not None:
            dupe_str = dupe_str + " " + self.correlation + "%"

        return dupe_str


class netem_loss:
    def __init__(self, base_loss='0', correlation=None):
        self.base_lat = base_loss
        self.correlation = correlation

    def __str__(self):
        loss_str = 'loss' + self.base_lat
        if self.correlation is not None:
            loss_str = loss_str + " " + self.correlation + "%"

        return loss_str


class netem_latency:
    def __init__(self, base_lat='0', jitter=None, correlation=None):
        self.base_lat = base_lat
        self.jitter = jitter
        self.correlation = correlation

    def __str__(self):
        delay_str = 'delay' + self.base_lat
        if self.jitter is not None:
            delay_str = delay_str + " " + self.jitter

        if self.correlation is not None:
            delay_str = delay_str + " " + self.correlation + "%"

        return delay_str


class ip_traffic_class:

    def __init__(self, ip, in_id, out_id, parent_id):
        self.ip = ip
        self.in_id = in_id
        self.out_id = out_id
        self.parent_id = parent_id
        self.stage_changed_ms = 0
        self.in_rate = '10024'
        self.out_rate = '10024'

        self.in_dupe = netem_dupe()
        self.in_loss = netem_loss()
        self.in_corrupt = netem_corrupt()
        self.in_lat = netem_latency()

        self.out_dupe = netem_dupe()
        self.out_loss = netem_loss()
        self.out_corrupt = netem_corrupt()
        self.out_lat = netem_latency()

        return

    def set_script_id(self, script_id):
        self.script_id = script_id

    def set_script_stage(self, script_stage_id):
        self.script_stage_id = script_stage_id

    def get_last_stage_change_ms(self):
        return self.stage_changed_ms
