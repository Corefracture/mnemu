import logging

import mnemu
import ip_filter
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

master_mnemu = mnemu.MNemu("ens192")

master_mnemu.add_new_ip("192.168.40.34")



master_mnemu.set_ip_bandwidth("192.168.40.34", 2500, True)

master_mnemu.set_ip_bandwidth("192.168.40.34", 25000, False)
master_mnemu.set_netem_setting_value("192.168.40.34", ip_filter.NetemType.LATENCY, 100, False)
#master_mnemu.set_netem_setting_value("192.168.40.34", ip_filter.NetemType.LATENCY, 100, True)

master_mnemu.set_netem_setting_value("192.168.40.34", ip_filter.NetemType.CORRUPT, 0.75, True)
master_mnemu.set_netem_setting_corr("192.168.40.34", ip_filter.NetemType.CORRUPT, 25.75, True)
master_mnemu.set_netem_setting_value("192.168.40.34", ip_filter.NetemType.DUPE, 0.75, True)




