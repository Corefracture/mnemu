import logging

LOGGER = logging.getLogger(__name__)


class NetemAtrrib:
    def __init__(self, val, corr_percent=None):
        self._base_val = val
        self._corr_percent = corr_percent
        self._attrib_str = None

    def set(self, val):
        try:
            #verify the cast to float so we ensure we're dealing with proper values
            float(val)
            self._base_val = str(val)
        except Exception as exp:
            # TODO: Logging for exp here
            return

    def get_val(self):
        return self._base_val

    def set_corr_percent(self, corr_percent):
        try:
            self._corr_percent = float(corr_percent)
        except Exception as exp:
            # TODO: cf: Logging for exp
            return

    def get_corr_percent(self):
        return self._corr_percent

    def __str__(self):
        if self._base_val == "0":
            return ""

        attrib_str = '{0} {1}'.format(self._attrib_str, self._base_val)

        if self._corr_percent is not None:
            attrib_str = "{0} {1}%".format(attrib_str, self._corr_percent)

        return attrib_str


class NetemCorrupt(NetemAtrrib):
    def __init__(self, base_corrupt='0', correlation=None):
        NetemAtrrib.__init__(self, base_corrupt, correlation)
        self._attrib_str = "corrupt"


class NetemReorder(NetemAtrrib):
    def __init__(self, base_reorder='0', correlation=None):
        NetemAtrrib.__init__(self, base_reorder, correlation)
        self._attrib_str = "reorder"


class NetemDupe(NetemAtrrib):
    def __init__(self, base_dupe='0', correlation=None):
        NetemAtrrib.__init__(self, base_dupe, correlation)
        self._attrib_str = "duplicate"


class NetemLoss(NetemAtrrib):
    def __init__(self, base_loss='0', correlation=None):
        NetemAtrrib.__init__(self, base_loss, correlation)
        self._attrib_str = "loss"


class NetemJitter(NetemAtrrib):
    def __init__(self, base_lat='0', correlation=None):
        NetemAtrrib.__init__(self, base_lat, correlation)
        # JITTER IS SET WITH DELAY, therefor do not set attrib name or correlation
        self._attrib_str = ""


class NetemLatency(NetemAtrrib):
    def __init__(self, base_lat='0', correlation=None):
        NetemAtrrib.__init__(self, base_lat, correlation)
        self._attrib_str = "delay"
