import ipaddress

from tc_cmds import *

server_ip = '192.168.86.42'

net = ipaddress.ip_network('192.168.86.179')

for a in net:
    print(str(a))

debug_tc_showqdiscs()
tc_clear_root_qdisc("enp0s3")
tc_create_root_tokenbucket_qdisc("enp0s3", '9999')

count = 0
for a in net:
    if str(a) == '192.168.86.42':
        continue
    last = int(str(a).split('.')[3])

    tc_create_ip_traffic_class('enp0s3', str(last + count), '9999', '10024')
    tc_create_ip_filter('enp0s3', str(a), '9999', str(last + count), False)

    count = count + 1
    tc_create_ip_traffic_class('enp0s3', str(last + count), '9999', '10024')
    tc_create_ip_filter('enp0s3', str(a), '9999', str(last + count), True)

    print(str(a))
    count = count + 1

debug_tc_showqdiscs()
# tc_clear_root_qdisc('enp0s3')
