# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import netem_defs as NetEm

class MNemuPresets:
    def __init__(self):
        self._preset_names = {}
        self._preset_data = {}
        self._add_hardcoded_presets()

    def get_preset_names(self):
        return self._preset_names

    def get_preset(self, preset_id):
        if preset_id in self._preset_names:
            return self._preset_data[preset_id]
        else:
            return None

    def _add_hardcoded_presets(self):

        # Mobile Terrible
        id = "MobileTerrible"
        display_name = "Terrible Mobile"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(768)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "175")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "1.50")
        self._preset_names[id] = display_name
        self._preset_data[id] = setting_data

        #3G
        id = "3G"
        display_name = "Mobile 3G"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(1500)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "100")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.75")
        self._preset_names[id] = display_name
        self._preset_data[id] = setting_data

        #3G Low Signal
        id = "3GLow"
        display_name = "Mobile 3G Low-Signal"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(700)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "150")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.85")
        self._preset_names[id] = display_name
        self._preset_data[id] = setting_data



