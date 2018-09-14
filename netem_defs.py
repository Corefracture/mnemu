import logging
from enum import Enum

LOGGER = logging.getLogger(__name__)


class NetemType(Enum):
    LATENCY = "0"
    JITTER = "1"
    DUPE = "2"
    LOSS = "3"
    REORDER = "4"
    CORRUPT = "5"
    BANDWIDTH = "6"

class NetemSettings:
    def __init__(self):
        self._rate = '1000000'
        self._loss = NetemLoss()
        self._dupe = NetemDupe()
        self._reorder = NetemReorder()
        self._corrupt = NetemCorrupt()
        self._latency = NetemLatency()
        self._jitter = NetemJitter()

    def netem_setting(self, setting_type, set_val=None):
        if setting_type == NetemType.LATENCY:
            if(set_val is not None):
                self._latency.set(set_val)
            return self._latency
        if setting_type is NetemType.JITTER:
            if(set_val is not None):
                self._jitter.set(set_val)
            return self._jitter
        if setting_type is NetemType.CORRUPT:
            if(set_val is not None):
                self._corrupt.set(set_val)
            return self._corrupt
        if setting_type is NetemType.LOSS:
            if(set_val is not None):
                self._loss.set(set_val)
            return self._loss
        if setting_type is NetemType.DUPE:
            if(set_val is not None):
                self._dupe.set(set_val)
            return self._dupe
        if setting_type is NetemType.REORDER:
            if(set_val is not None):
                self._reorder.set(set_val)
            return self._reorder
        if setting_type is NetemType.BANDWIDTH:
            if(set_val is not None):
                self.set_bandwidth(set_val)
            return self._rate

    def set_bandwidth(self, rate_kbps):
        try:
            rate_kbps = str(int(float(rate_kbps)))
            self._rate = rate_kbps
            return self._rate
        except Exception as exp:
            print(exp.__str__())
            #TODO: cf: logging
            return

    def set_setting(self, setting_type, setting_val):
        self.netem_setting(NetemType(setting_type), set_val=setting_val)

class NetemAtrrib:
    def __init__(self, val, corr_percent=None):
        self._base_val = val
        self._corr_percent = corr_percent
        self._attrib_str = None

    @staticmethod
    def is_base_val_zero(val):
        try:
            test = float(val)
            return test <= 0
        except Exception as exp:
            return True

    def set(self, val):
        try:
            #verify the cast to float so we ensure we're dealing with proper values
            #and add prefix 0's if there aren't any
            self._base_val = str(float(val))
        except Exception as exp:
            self._base_val = "0"
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
        if NetemAtrrib.is_base_val_zero(self._base_val) is True:
            return ""

        attrib_str = '{0} {1}%'.format(self._attrib_str, self._base_val)

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


class NetemLatency(NetemAtrrib):
    def __init__(self, base_lat='0', correlation=None):
        NetemAtrrib.__init__(self, base_lat, correlation)
        self._attrib_str = "delay"

    def __str__(self):
        if NetemAtrrib.is_base_val_zero(self._base_val):
            self._base_val = "0"
        attrib_str = '{0} {1}ms'.format(self._attrib_str, self._base_val)

        return attrib_str

class NetemJitter(NetemAtrrib):
    def __init__(self, base_lat='0', correlation=None):
        NetemAtrrib.__init__(self, base_lat, correlation)
        # JITTER IS SET WITH DELAY, therefor do not set attrib name or correlation
        self._attrib_str = ""

    def __str__(self):
        if NetemAtrrib.is_base_val_zero(self._base_val):
            return ""
        attrib_str = '{0}ms'.format(self._base_val)

        return attrib_str