# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details


import copy

from mnemu import netem_defs as netem
from mnemu.netem_defs import NetemType


class IPSettings:
    """
    IPSettings holds the current settings for a specific IP address
    """

    def __init__(self, ip, in_id, out_id):

        self.ip = ip
        self.in_id = in_id
        self.out_id = out_id
        self.stage_changed_ms = 0
        self.in_netem = netem.NetemSettings()
        self.out_netem = netem.NetemSettings()

        self.script_id = None
        self.script_stage_id = None

    def get_in_rate(self):
        return self.in_netem.netem_setting(NetemType.BANDWIDTH)

    def get_out_rate(self):
        return self.out_netem.netem_setting(NetemType.BANDWIDTH)

    def set_netem_settings(self, netem_settings, inbound=True):
        if inbound is True:
            self.in_netem = copy.deepcopy(netem_settings)
        else:
            self.out_netem = copy.deepcopy(netem_settings)

    def set_bandwidth(self, rate, inbound=True):
        try:
            # Verify value is an actual number
            netem_settings = self.in_netem if inbound is True else self.out_netem
            int(rate)
            netem_settings.set_bandwidth(rate)
        except Exception as exp:
            return
            # TODO: cf: Logging excep here

    def set_netem_setting(self, setting_type, setting_val, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        set_to_val = netem_settings.netem_setting(netem.NetemType(setting_type), setting_val)
        return set_to_val

    def get_netem_setting(self, setting_type, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        return netem_settings.netem_setting(netem.NetemType(setting_type))


    def set_netem_setting_corr(self, setting_type, setting_correlation, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.netem_setting(netem.NetemType(setting_type))
        netem_type_set.set_corr_percent(setting_correlation)
        return netem_type_set.get_corr_percent()

    def get_netem_setting_corr(self, setting_type, inbound=True):
        netem_settings = self.in_netem if inbound is True else self.out_netem
        netem_type_set = netem_settings.netem_setting(netem.NetemType(setting_type))
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
            setting = netem_sets.netem_setting(NetemType.LATENCY).__str__()
            jitter = netem_sets.netem_setting(NetemType.JITTER).__str__()

            if setting is not "" or jitter is not "":
                if setting is "" and jitter is not "":
                    setting = "0ms"

                if(jitter is not ""):
                    setting = setting + " " + jitter
                ret_val = ret_val + setting

            setting = netem_sets.netem_setting(NetemType.REORDER).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.netem_setting(NetemType.LOSS).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.netem_setting(NetemType.DUPE).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting
            setting = netem_sets.netem_setting(NetemType.CORRUPT).__str__()
            if setting is not "":
                ret_val = ret_val + " " + setting

        if ret_val is None or ret_val == "":
            return ret_val

        ret_val = ret_val.lstrip()
        ret_val = ret_val.rstrip()

        return str(ret_val)

    def _get_netemvals_as_dict(self, inbound=True):
        ret_val = {}
        ns = self.in_netem if inbound is True else self.out_netem
        prefix = "in_" if inbound is True else "out_"
        ret_val[prefix + "loss"] = ns.netem_setting(NetemType.LOSS).get_val()
        ret_val[prefix + "latency"] = ns.netem_setting(NetemType.LATENCY).get_val()
        ret_val[prefix + "dupe"] = ns.netem_setting(NetemType.DUPE).get_val()
        ret_val[prefix + "reord"] = ns.netem_setting(NetemType.REORDER).get_val()
        ret_val[prefix + "corrupt"] = ns.netem_setting(NetemType.CORRUPT).get_val()
        ret_val[prefix + "jitter"] = ns.netem_setting(NetemType.JITTER).get_val()

        return ret_val

    def dict(self):
        ret_val_dict = {}
        ret_val_dict["in_bandwidth"] = self.get_in_rate()
        ret_val_dict["out_bandwidth"] = self.get_out_rate()
        ret_val_dict.update(self._get_netemvals_as_dict(True))
        ret_val_dict.update(self._get_netemvals_as_dict(False))

        return ret_val_dict
