# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

from mnemu import netem_defs as NetEm


class MNemuPresets:
    def __init__(self):
        self._preset_download_names = {}
        self._preset_download_data = {}
        self._preset_upload_names = {}
        self._preset_upload_data = {}

        self._add_hardcoded_presets(self._preset_download_names, self._preset_download_data)
        self._add_hardcoded_upload_presets(self._preset_upload_names, self._preset_upload_data)

    def get_preset_names(self, upload=False):
        if upload is False:
            return self._preset_download_names
        else:
            return self._preset_upload_names

    def get_preset(self, preset_id, upload=False):
        data = self._preset_download_data if upload is False else self._preset_upload_data
        if preset_id in data:
            return data[preset_id]
        else:
            return None

    def _add_hardcoded_presets(self, names, data):

        # Mobile Terrible
        id = "Full"
        display_name = "Regular Network"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(100000)
        names[id] = display_name
        data[id] = setting_data

        # Mobile Terrible
        id = "MobileTerrible"
        display_name = "Terrible Mobile"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(640)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "175")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "1.50")
        names[id] = display_name
        data[id] = setting_data

        # 2G
        id = "2G"
        display_name = "Mobile 2G"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(256)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "75")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.50")
        names[id] = display_name
        data[id] = setting_data

        #3G
        id = "3G"
        display_name = "Mobile 3G"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(1500)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "75")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.15")
        names[id] = display_name
        data[id] = setting_data

        #3G Low Signal
        id = "3GLow"
        display_name = "Mobile 3G - Low Signal"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(700)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "100")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.50")
        names[id] = display_name
        data[id] = setting_data

        # 3G High latency
        id = "3G"
        display_name = "Mobile 3G - High Latency"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(1500)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "150")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.25")
        names[id] = display_name
        data[id] = setting_data

        # 4G Low End
        id = "4G"
        display_name = "Mobile 4G - Low End"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(35000)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "10")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.01")
        names[id] = display_name
        data[id] = setting_data

    def _add_hardcoded_upload_presets(self, names, data):
        # Mobile Terrible
        id = "Full"
        display_name = "Regular Network"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(100000)
        names[id] = display_name
        data[id] = setting_data

        # Mobile Terrible
        id = "MobileTerrible"
        display_name = "Terrible Mobile"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(256)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "200")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "1.50")
        names[id] = display_name
        data[id] = setting_data

        # 2G
        id = "2G"
        display_name = "Mobile 2G"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(75)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "75")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.25")
        names[id] = display_name
        data[id] = setting_data

        # 3G
        id = "3G"
        display_name = "Mobile 3G"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(768)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "50")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.15")
        names[id] = display_name
        data[id] = setting_data

        # 3G Low Signal
        id = "3GLow"
        display_name = "Mobile 3G - Low Signal"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(650)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "100")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.75")
        names[id] = display_name
        data[id] = setting_data

        # 3G High latency
        id = "3G"
        display_name = "Mobile 3G - High Latency"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(768)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "150")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.50")
        names[id] = display_name
        data[id] = setting_data

        # 4G Low End
        id = "4G"
        display_name = "Mobile 4G - Low End"
        setting_data = NetEm.NetemSettings()
        setting_data.set_bandwidth(25000)
        setting_data.netem_setting(NetEm.NetemType.LATENCY, "10")
        setting_data.netem_setting(NetEm.NetemType.LOSS, "0.01")
        names[id] = display_name
        data[id] = setting_data
