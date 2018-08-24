import logging

import ip_filter
import tc

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class MNemu:
    def __init__(self, iface, root_id):
        self._master_ip_settings = {}
        self._iface_name = iface
        self._root_id = root_id
        self._next_id = 0

        self._reset_tc(iface)
        self._add_root_qdisc(iface)

    def _add_root_qdisc(self, iface):
        tc.tc_create_root_tokenbucket_qdisc(iface, self._root_id)

    def _reset_tc(self, iface):
        tc.tc_reset(iface)

    def get_ip_settings(self, ip):
        ip_settings = None
        if ip not in self._master_ip_settings:
            # Create the entries for this
            ip_settings = self.add_new_ip(ip)
        else:
            ip_settings = self._master_ip_settings[ip]

        return ip_settings

    def add_new_ip(self, ip):
        if ip in self._master_ip_settings:
            return self._master_ip_settings[ip]

        inbound_id = str(self._next_id + 1)
        outbound_id = str(self._next_id + 2)
        self._next_id = self._next_id + 3

        ip_setting = ip_filter.IPTrafficFilter(ip, inbound_id, outbound_id, self._root_id)

        tc.tc_create_ip_traffic_class(self._iface_name, inbound_id, self._root_id, ip_setting.get_in_rate())
        tc.tc_create_ip_traffic_class(self._iface_name, outbound_id, self._root_id, ip_setting.get_out_rate())

        tc.tc_create_ip_filter(self._iface_name, ip, self._root_id, inbound_id, True)
        tc.tc_create_ip_filter(self._iface_name, ip, self._root_id, outbound_id, False)

        tc.tc_create_netem_qdisc(self._iface_name, ip, ip_setting.get_netem_inbound_cmd(), inbound_id,
                                 self._root_id + ":" + inbound_id)
        tc.tc_create_netem_qdisc(self._iface_name, ip, ip_setting.get_netem_outbound_cmd(), outbound_id,
                                 self._root_id + ":" + outbound_id)

        self._master_ip_settings[ip] = ip_setting

        return ip_setting

    def clear_ip_rules(self, ip):
        return
        # TODO: cf: clear rules

    def set_netem_setting_value(self, ip, setting_type, val, inbound=True):
        val_set_to = 0
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            val_set_to = ip_settings.set_netem_setting(setting_type, val, inbound)
        else:
            return
            # TODO: cf: Log IP not found

        return val_set_to

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
        corr_set_to = 0
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
        rate_set_to = 0
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]

            if inbound is True:
                ip_settings.set_in_rate(rate)
                rate_set_to = ip_settings.get_in_rate()
            else:
                ip_settings.set_out_rate(rate)
                rate_set_to = ip_settings.get_out_rate()
        else:
            # TODO: cf: logging around not found IP
            return

        return rate_set_to

    def get_known_ips(self):
        return list(self._master_ip_settings)
