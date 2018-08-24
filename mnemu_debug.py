import logging

import mnemu

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

master_mnemu = mnemu.MNemu("enp0s3", '9999')

master_mnemu.add_new_ip("192.168.1.1")
