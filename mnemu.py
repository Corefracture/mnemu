# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import logging
import time

import ip_filter
import tc_cmds
from mnemu_presets import MNemuPresets

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class MNemu:

    REFRESH_ALLOWED_INTERVAL_SECS = 10

    def __init__(self, iface):
        self._master_ip_settings = {}
        self._iface_device = iface
        self._ifb_device = "ifb0"
        self._iface_device_root_id = "9998"
        self._ifb_device_root_id = "9999"

        self._next_qdisc_id = 0

        self._reset_tc(self._iface_device)
        self._setup_virtual_device()
        self._setup_ingress_virt_rules()
        self._add_root_qdisc(self._ifb_device, self._ifb_device_root_id)
        self._add_root_qdisc(self._iface_device, self._iface_device_root_id)

        self._presets = MNemuPresets()

        self._rules_last_reset_time = time.time()



    def refresh_tc(self):
        self._reset_tc(self._ifb_device)
        self._setup_ingress_virt_rules()
        self._add_root_qdisc(self._ifb_device, self._ifb_device_root_id)
        self._add_root_qdisc(self._iface_device, self._iface_device_root_id)

        for ip, ip_setting in self._master_ip_settings.items():
            self._set_ip_settings_in_tc(ip, ip_setting)


    def _set_ip_settings_in_tc(self, ip, ip_setting):
        inbound_id = ip_setting.in_id
        outbound_id = ip_setting.out_id

        tc_cmds.tc_create_ip_traffic_class(self._iface_device, inbound_id, self._iface_device_root_id,
                                           ip_setting.get_in_rate())
        tc_cmds.tc_create_ip_traffic_class(self._ifb_device, outbound_id, self._ifb_device_root_id,
                                           ip_setting.get_out_rate())

        tc_cmds.tc_create_ip_filter(self._iface_device, ip, self._iface_device_root_id, inbound_id, True)
        tc_cmds.tc_create_ip_filter(self._ifb_device, ip, self._ifb_device_root_id, outbound_id, False)

        tc_cmds.tc_update_netem_qdisc(self._iface_device, ip, ip_setting.get_netem_inbound_cmd(), inbound_id,
                                      self._iface_device_root_id)
        tc_cmds.tc_update_netem_qdisc(self._ifb_device, ip, ip_setting.get_netem_outbound_cmd(), outbound_id,
                                      self._ifb_device_root_id)

    def _setup_virtual_device(self):
        tc_cmds.rem_virtual_iface(self._ifb_device)
        tc_cmds.create_virtual_iface(self._ifb_device)

    def _setup_ingress_virt_rules(self):
        self._reset_tc(self._ifb_device)
        tc_cmds.tc_add_ingress_qdisc(self._iface_device)
        tc_cmds.tc_create_virt_redirect_filter(self._iface_device, self._ifb_device)

    def _add_root_qdisc(self, iface, root_id):
        tc_cmds.tc_create_root_tokenbucket_qdisc(iface, root_id)

    def _reset_tc(self, iface):
        tc_cmds.tc_reset(iface)
        tc_cmds.tc_ingress_reset(iface)

    def get_ip_settings(self, ip):
        if ip not in self._master_ip_settings:
            # Create the entries for this
            ip_settings = self.add_new_ip(ip)
        else:
            ip_settings = self._master_ip_settings[ip]

        return ip_settings

    def add_new_ip(self, ip):
        if ip in self._master_ip_settings:
            return self._master_ip_settings[ip]

        outbound_id = str(self._next_qdisc_id + 1)
        inbound_id = str(self._next_qdisc_id + 2)
        self._next_qdisc_id = self._next_qdisc_id + 3

        ip_setting = ip_filter.IPTrafficFilter(ip, inbound_id, outbound_id)

        self._set_ip_settings_in_tc(ip, ip_setting)

        self._master_ip_settings[ip] = ip_setting

        return ip_setting

    def set_netem_setting_from_preset(self, ip, netem_settings, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            ip_settings.set_netem_settings(netem_settings, inbound)
            if inbound is True:
                rate_set_to = ip_settings.get_in_rate()
                tc_cmds.tc_change_ip_traffic_class(self._iface_device, ip_settings.in_id, self._iface_device_root_id, rate_set_to)

            else:
                rate_set_to = ip_settings.get_out_rate()
                tc_cmds.tc_change_ip_traffic_class(self._ifb_device, ip_settings.out_id, self._ifb_device_root_id, rate_set_to)

            self.update_netem_qdisc(ip, inbound)

    def clear_ip_rules(self, ip):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            inbound_id = ip_settings.in_id
            outbound_id = ip_settings.out_id
            self._master_ip_settings[ip] = ip_filter.IPTrafficFilter(ip, inbound_id, outbound_id)
            self.set_ip_bandwidth(ip, self.get_ip_bandwidth(ip, True), True)
            self.set_ip_bandwidth(ip, self.get_ip_bandwidth(ip, False), False)
            self.update_netem_qdisc(ip, True)
            self.update_netem_qdisc(ip, False)


    def set_netem_setting_value(self, ip, setting_type, val, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            val_set_to = ip_settings.set_netem_setting(setting_type, val, inbound)
            self.update_netem_qdisc(ip, inbound)
        else:
            return
            # TODO: cf: Log IP not found

        return val_set_to

    def update_netem_qdisc(self, ip, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            if inbound is True:
                netem_cmd = ip_settings.get_netem_inbound_cmd()
                iface = self._iface_device
                qdisc_id = ip_settings.in_id
                root_id = self._iface_device_root_id
            else:
                netem_cmd = ip_settings.get_netem_outbound_cmd()
                iface = self._ifb_device
                qdisc_id = ip_settings.out_id
                root_id = self._ifb_device_root_id

            tc_cmds.tc_update_netem_qdisc(iface, ip, netem_cmd, qdisc_id, root_id)

    def get_netem_setting_value(self, ip, setting_type, inbound=True):
        val_set_to = 0
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            val_set_to = ip_settings.get_netem_setting(setting_type, inbound)
        else:
            return
            # TODO: cf: Log IP not found

        return val_set_to

    def set_netem_setting_corr(self, ip, setting_type, corr_val, inbound=True):
        corr_set_to = 0
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            corr_set_to = ip_settings.set_netem_setting_corr(setting_type, corr_val, inbound)
        else:
            return
            # TODO: cf: Log IP not found

        return corr_set_to

    def get_netem_setting_corr(self, ip, setting_type, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            corr_set_to = ip_settings.get_netem_setting_corr(setting_type, inbound)
        else:
            return
            # TODO: cf: Log IP not found

        return corr_set_to

    def get_ip_bandwidth(self, ip, inbound=True):
        rate = 0
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            if inbound is True:
                rate = ip_settings.get_in_rate()
            else:
                rate = ip_settings.get_out_rate()
        else:
            # TODO: cf: logging around not found IP
            return

        return rate

    def set_ip_bandwidth(self, ip, rate, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            ip_settings.set_bandwidth(rate, inbound)
            if inbound is True:
                rate_set_to = ip_settings.get_in_rate()
                tc_cmds.tc_change_ip_traffic_class(self._iface_device, ip_settings.in_id, self._iface_device_root_id, rate_set_to)

            else:
                rate_set_to = ip_settings.get_out_rate()
                tc_cmds.tc_change_ip_traffic_class(self._ifb_device, ip_settings.out_id, self._ifb_device_root_id, rate_set_to)

        else:
            # TODO: cf: logging around not found IP
            return

        return rate_set_to

    def get_known_ips(self):
        return list(self._master_ip_settings)
