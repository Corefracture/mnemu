# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import subprocess



def log_raw_output(stdout, stderr):
    print("STDOUT: " + str(stdout))
    print("STDERR: " + str(stderr))


def _execute_task(*params):
    try:
        print(params)
        process = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        stdout = output[0]
        stderr = ""
        if (len(output) > 1):
            stderr = output[1]

        log_raw_output(stdout, stderr)
    except Exception as exp:
        return "ERROR!", exp.__str__()

    return stdout, stderr


def _mod_probe_ifb_rem():
    return _execute_task("modprobe", "-r", "ifb")


def _mod_probe_ifb_create():
    return _execute_task("modprobe", "ifb", "numifbs=1")


def _set_ip_link_virt_device(vir_iface_name, set_up=True):
    up_or_down = "up" if set_up is True else "down"
    return _execute_task('ip', 'link', 'set', 'dev', vir_iface_name, up_or_down)


def rem_virtual_iface(vir_iface_name):
    try:
        _set_ip_link_virt_device(vir_iface_name, False)
        _mod_probe_ifb_rem()
    except Exception as ex:
        #TODO: LOG
        return


def create_virtual_iface(vir_iface_name):
    try:
        _mod_probe_ifb_create()
        _set_ip_link_virt_device(vir_iface_name, True)
    except Exception as ex:
        #TODO: LOG
        return

def tc_reset(iface):
    stdout, stderr = _execute_task("tc", "qdisc", "del", "root", "dev", iface)

    log_raw_output(stdout, stderr)

def tc_ingress_reset(iface):
    stdout, stderr = _execute_task("tc", "qdisc", "del", "dev", iface, "ingress")

    log_raw_output(stdout, stderr)


def tc_create_root_tokenbucket_qdisc(iface, qdiscid):
    stdout, stderr = _execute_task("tc", "qdisc", "add", "dev", iface, "root", "handle", qdiscid + ":", "htb")
    log_raw_output(stdout, stderr)


def tc_create_ip_traffic_class(iface, classid, parent_qdiscid, rate_kbit):
    parent_qdiscid = parent_qdiscid + ":"
    classid = parent_qdiscid + classid
    stdout, stderr = _execute_task("tc", "class", "add", "dev", iface, "parent", str(parent_qdiscid), "classid",
                                     classid, "htb", "rate", str(rate_kbit) + "kbit")


def tc_change_ip_traffic_class(iface, classid, parent_qdiscid, rate_kbit):
    parent_qdiscid = parent_qdiscid + ":"
    classid = parent_qdiscid + classid
    stdout, stderr = _execute_task("tc", "class", "change", "dev", iface, "parent", parent_qdiscid, "classid",
                                     classid, "htb", "rate", str(rate_kbit) + "kbit")


def tc_remove_filters(iface, prnt_class_id):
    prnt_class_id = prnt_class_id + ":"

    stdout, stderr = _execute_task("tc", "filter", "del", "dev", iface, "parent", prnt_class_id)

    return

def tc_create_incoming_filter(iface, ip, prnt_qdisc_id, prnt_class_id, ip_is_dst=False):
    prnt_qdisc_id = prnt_qdisc_id + ":"
    prnt_class_id = prnt_qdisc_id + prnt_class_id
    origin = 'src' if ip_is_dst is True else 'dst'

    stdout, stderr = _execute_task("tc", "filter", "add", "dev", iface, "parent", prnt_qdisc_id,
                                     "protocol", "ip", "prio", "1", "u32", "flowid", prnt_class_id,
                                    "match", "ip", origin, ip)
    return


def tc_create_ip_filter(iface, ip, prnt_qdisc_id, prnt_class_id, ip_is_dst=False):
    prnt_qdisc_id = prnt_qdisc_id + ":"
    prnt_class_id = prnt_qdisc_id + prnt_class_id
    origin = 'dst' if ip_is_dst is True else 'src'

    stdout, stderr = _execute_task("tc", "filter", "add", "dev", iface, "parent", prnt_qdisc_id,
                                     "protocol", "ip", "prio", "1", "u32", "flowid", prnt_class_id,
                                    "match", "ip", origin, ip)

    return

def tc_create_virt_redirect_filter(iface, virt_iface):
    return _execute_task("tc", "filter", "add", "dev", iface, "parent", "ffff:",
                                     "protocol", "ip", "u32", "match", "u32", "0", "0", "action",
                                     "mirred", "egress", "redirect", "dev", virt_iface)


def tc_add_ingress_qdisc(iface):
    return _execute_task("tc", "qdisc", "add", "dev", iface, "handle", "ffff:", "ingress")


def tc_update_netem_qdisc(iface, ip, netem_def, qdisc_id, prnt_qdisc_id):
    tc_remove_netem_qdisc(iface, qdisc_id, prnt_qdisc_id + ":" + qdisc_id)
    if netem_def is None or netem_def == "":
        return ""
        #return _execute_task("tc", "qdisc", "add", "dev", iface, "parent", prnt_qdisc_id + ":" + qdisc_id,
        # "handle", qdisc_id + ":", "netem")
    else:
        return _execute_task("tc", "qdisc", "add", "dev", iface, "parent", prnt_qdisc_id + ":" + qdisc_id,
                             "handle", qdisc_id + ":", "netem", *netem_def.split(" "))

def tc_remove_ingress_qdisc(iface):
    return _execute_task("tc", "qdisc", "del", "dev", iface, "ingress")


def tc_remove_netem_qdisc(iface, qdisc_id, prnt_qdisc_id):
    return _execute_task("tc", "qdisc", "del", "dev", iface, "parent", prnt_qdisc_id,
                                     "handle", qdisc_id + ":", )

def debug_tc_showqdiscs():
    stdout, stderr = _execute_task("tc", "qdisc")
    log_raw_output(stdout, stderr)
