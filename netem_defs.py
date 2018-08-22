class NetemCorrupt:
    def __init__(self, base_corrupt='0', correlation=None):
        self.base_corrupt = base_corrupt
        self.correlation = correlation

    def __str__(self):
        corrupt_str = 'corrupt' + self.base_corrupt
        if self.correlation is not None:
            corrupt_str = corrupt_str + " " + self.correlation + "%"

        return corrupt_str


class NetemReorder:
    def __init__(self, base_reorder='0', correlation=None):
        self.base_reorder = base_reorder
        self.correlation = correlation

    def __str__(self):
        reorder_str = 'reorder' + self.base_reorder
        if self.correlation is not None:
            reorder_str = reorder_str + " " + self.correlation + "%"

        return reorder_str


class NetemDupe:
    def __init__(self, base_dupe='0', correlation=None):
        self.base_dupe = base_dupe
        self.correlation = correlation

    def __str__(self):
        dupe_str = 'duplicate' + self.base_dupe
        if self.correlation is not None:
            dupe_str = dupe_str + " " + self.correlation + "%"

        return dupe_str


class NetemLoss:
    def __init__(self, base_loss='0', correlation=None):
        self.base_lat = base_loss
        self.correlation = correlation

    def __str__(self):
        loss_str = 'loss' + self.base_lat
        if self.correlation is not None:
            loss_str = loss_str + " " + self.correlation + "%"

        return loss_str


class NetemLatency:
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