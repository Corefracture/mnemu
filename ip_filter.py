import json
from enum import Enum

import netem_defs as nems


class NetemType(Enum):
    LATENCY = "0"
    JITTER = "1"
    DUPE = "2"
    LOSS = "3"
    REORDER = "4"
    CORRUPT = "5"

class NetemSettings:
    def __init__(self):
        self._loss = nems.NetemLoss()
        self._dupe = nems.NetemDupe()
        self._reorder = nems.NetemReorder()
        self._corrupt = nems.NetemCorrupt()
        self._latency = nems.NetemLatency()
        self._jitter = nems.NetemJitter()

    def get_netem_setting(self, setting_type):
        if setting_type is NetemType.LATENCY:
            return self._latency
        if setting_type is NetemType.JITTER:
            return self._jitter
        if setting_type is NetemType.CORRUPT:
            return self._corrupt
        if setting_type is NetemType.LOSS:
            return self._loss
        if setting_type is NetemType.DUPE:
            return self._dupe
        if setting_type is NetemType.REORDER:
            return self._reorder


class IPTrafficFilter:
    """
    IPTrafficFilter holds the current settings for a specific IP address
    """

    def __init__(self, ip, in_id, out_id, parent_id):

        self.ip = ip
        self.in_id = in_id
        self.out_id = out_id
        self.parent_id = parent_id
        self.stage_changed_ms = 0
        self._in_rate = '10000'
        self._out_rate = '10000'

        self.in_netem = NetemSettings()
        self.out_netem = NetemSettings()

        self.script_id = None
        self.script_stage_id = None

    def get_in_rate(self):
        return self._in_rate

    def get_out_rate(self):
        return self._out_rate

    def set_in_rate(self, rate):
        try:
            # Verify value is an actual number
            int(rate)
            self._in_rate = rate
        except:
            return
            # TODO: cf: Logging excep here

    def set_out_rate(self, rate):
        try:
            # Verify value is an actual number
            int(rate)
            self._out_rate = rate
        except:
            return
            # TODO: cf: Logging excep here

    def set_netem_setting(self, setting_type, setting_val, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.get_netem_setting(setting_type)
        netem_type_set.set(setting_val)

        return netem_type_set.get_val()

    def get_netem_setting(self, setting_type, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.get_netem_setting(setting_type)

        return netem_type_set.get_val()

    def set_netem_setting_corr(self, setting_type, setting_correlation, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.get_netem_setting(setting_type)
        netem_type_set.set_corr_percent(setting_correlation)

        return netem_type_set.get_corr_percent()

    def get_netem_setting_corr(self, setting_type, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.get_netem_setting(setting_type)

        return netem_type_set.get_corr_percent()

    def set_script_id(self, script_id):
        self.script_id = script_id

    def set_script_stage(self, script_stage_id):
        self.script_stage_id = script_stage_id

    def get_last_stage_change_ms(self):
        return self.stage_changed_ms

    def get_netem_inbound_cmd(self):
        return self._build_netem_cmd()

    def get_netem_outbound_cmd(self):
        return self._build_netem_cmd(False)

    def _build_netem_cmd(self, inbound=True):
        netem_sets = self.in_netem if inbound is True else self.out_netem
        ret_val = ""

        if netem_sets is not None:
            ret_val = ""
            setting = netem_sets.get_netem_setting(NetemType.LATENCY).__str__()
            if setting is not "":
                jitter = netem_sets.get_netem_setting(NetemType.JITTER)
                if jitter.get_val() is not "0":
                    # insert the jitter value in the middle
                    setting_split = setting.split(' ')
                    setting_split.insert(1, jitter.get_val())
                    setting = " ".join(setting_split)

                ret_val = ret_val + setting

            setting = netem_sets.get_netem_setting(NetemType.REORDER).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.get_netem_setting(NetemType.LOSS).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.get_netem_setting(NetemType.DUPE).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.get_netem_setting(NetemType.CORRUPT).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting

        return ret_val

    def get_netemvals_as_dict(self, inbound=True):
        ret_val = {}
        netem_settings = self.in_netem if inbound is True else self.out_netem
        ret_val["loss"] = netem_settings.get_netem_setting(NetemType.LOSS).get_val()
        ret_val["lat"] = netem_settings.get_netem_setting(NetemType.LATENCY).get_val()
        ret_val["dupe"] = netem_settings.get_netem_setting(NetemType.DUPE).get_val()
        ret_val["reord"] = netem_settings.get_netem_setting(NetemType.REORDER).get_val()
        ret_val["corru"] = netem_settings.get_netem_setting(NetemType.CORRUPT).get_val()
        ret_val["jitter"] = netem_settings.get_netem_setting(NetemType.JITTER).get_val()

        return ret_val

    def web_str(self):
        ret_val_dict = {}
        ret_val_dict["in_rate"] = self.get_in_rate()
        ret_val_dict["out_rate"] = self.get_out_rate()
        ret_val_dict["in"] = self.get_netemvals_as_dict(True)
        ret_val_dict["out"] = self.get_netemvals_as_dict(False)

        return json.dumps(ret_val_dict)
