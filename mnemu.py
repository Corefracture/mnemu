import logging

import ip_filter
import cmds

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class MNemu:
    def __init__(self, iface):
        self._master_ip_settings = {}
        self._iface_device = iface
        self._ifb_device = "ifb0"
        self._iface_device_root_id = "9998"
        self._ifb_device_root_id = "9999"

        self._next_qdisc_id = 0

        self._reset_tc(self._iface_device)
        self._setup_ingress_virt_rules()
        self._add_root_qdisc(self._ifb_device, self._ifb_device_root_id)
        self._add_root_qdisc(self._iface_device, self._iface_device_root_id)




    def _setup_ingress_virt_rules(self):
        cmds.rem_virtual_iface(self._ifb_device)
        cmds.create_virtual_iface(self._ifb_device)
        self._reset_tc(self._ifb_device)
        cmds.tc_add_ingress_qdisc(self._iface_device)
        cmds.tc_create_virt_redirect_filter(self._iface_device, self._ifb_device)

    def _add_root_qdisc(self, iface, root_id):
        cmds.tc_create_root_tokenbucket_qdisc(iface, root_id)

    def _reset_tc(self, iface):
        cmds.tc_reset(iface)

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

        cmds.tc_create_ip_traffic_class(self._iface_device, inbound_id, self._iface_device_root_id, ip_setting.get_in_rate())
        cmds.tc_create_ip_traffic_class(self._ifb_device, outbound_id, self._ifb_device_root_id, ip_setting.get_out_rate())

        cmds.tc_create_ip_filter(self._iface_device, ip, self._iface_device_root_id, inbound_id, True)
        cmds.tc_create_ip_filter(self._ifb_device, ip, self._ifb_device_root_id, outbound_id, False)

        cmds.tc_update_netem_qdisc(self._iface_device, ip, ip_setting.get_netem_inbound_cmd(), inbound_id,
                                   self._iface_device_root_id)
        cmds.tc_update_netem_qdisc(self._ifb_device, ip, ip_setting.get_netem_outbound_cmd(), outbound_id,
                                   self._ifb_device_root_id)

        self._master_ip_settings[ip] = ip_setting

        return ip_setting

    def clear_ip_rules(self, ip):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            cmds.tc_remove_netem_qdisc(self._iface_device, ip_settings.in_id, self._iface_device_root_id)
            cmds.tc_remove_netem_qdisc(self._ifb_device, ip_settings.out_id, self._ifb_device_root_id)
            self.set_ip_bandwidth(ip, 1000000, True)
            self.set_ip_bandwidth(ip, 1000000, False)
        return


    def set_netem_setting_value(self, ip, setting_type, val, inbound=True):
        if ip in self._master_ip_settings:
            ip_settings = self._master_ip_settings[ip]
            val_set_to = ip_settings.set_netem_setting(setting_type, val, inbound)
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

            cmds.tc_update_netem_qdisc(iface, ip, netem_cmd, qdisc_id, root_id)

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

            if inbound is True:
                ip_settings.set_in_rate(rate)
                cmds.tc_change_ip_traffic_class(self._iface_device, ip_settings.in_id, self._iface_device_root_id, rate)
                rate_set_to = ip_settings.get_in_rate()
            else:
                ip_settings.set_out_rate(rate)
                cmds.tc_change_ip_traffic_class(self._ifb_device, ip_settings.out_id, self._ifb_device_root_id, rate)
                rate_set_to = ip_settings.get_out_rate()


        else:
            # TODO: cf: logging around not found IP
            return

        return rate_set_to

    def get_known_ips(self):
        return list(self._master_ip_settings)
