import subprocess

TC_TC = "tc"
TC_NETEM = "netem"
TC_QDISC = "qdisc"
TC_DEV = "dev"
TC_FILTER = "filter"
TC_FLOWID = "flowid"
TC_CLASS = "class"
TC_CHANGE = "change"
TC_ADD = "add"
TC_DEL = "del"
TC_REPLACE = "replace"
TC_ROOT = "root"
TC_HNDL = "handle"
TC_PARNT = "parent"
TC_CLASSID = "classid"
TC_HTB = "htb"
TC_RATE = "rate"
TC_PROT = "protocol"
TC_IP = "ip"
TC_PRIO = "prio"


def log_raw_output(stdout, stderr):
    print("STDOUT: " + str(stdout))
    print("STDERR: " + str(stderr))


def _tc_execute_cmd(*params):
    params = ("tc",) + params
    print(params)
    stdout = ""
    stderr = ""

    try:
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


def tc_reset(iface):
    stdout, stderr = (_tc_execute_cmd(TC_QDISC, TC_DEL, TC_ROOT, TC_DEV, iface))

    log_raw_output(stdout, stderr)


def tc_create_root_tokenbucket_qdisc(iface, qdiscid):
    stdout, stderr = _tc_execute_cmd(TC_QDISC, TC_ADD, TC_DEV, iface, TC_ROOT, TC_HNDL, qdiscid + ":", "htb")
    log_raw_output(stdout, stderr)


def tc_create_ip_traffic_class(iface, classid, parent_qdiscid, rate_kbit):
    parent_qdiscid = parent_qdiscid + ":"
    classid = parent_qdiscid + classid
    stdout, stderr = _tc_execute_cmd(TC_CLASS, TC_ADD, TC_DEV, iface, TC_PARNT, str(parent_qdiscid), TC_CLASSID,
                                     classid, TC_HTB, TC_RATE, str(rate_kbit) + "kbit")


def tc_update_ip_traffic_class(iface, classid, parent_qdiscid, rate_kbit):
    parent_qdiscid = parent_qdiscid + ":"
    classid = parent_qdiscid + classid
    stdout, stderr = _tc_execute_cmd(TC_CLASS, TC_CHANGE, TC_DEV, iface, TC_PARNT, parent_qdiscid, TC_CLASSID,
                                     classid, TC_HTB, TC_RATE, rate_kbit + "kbit")


def tc_create_ip_filter(iface, ip, prnt_qdisc_id, prnt_class_id, ip_is_dst=False):
    prnt_qdisc_id = prnt_qdisc_id + ":"
    prnt_class_id = prnt_qdisc_id + prnt_class_id
    origin = 'dst' if ip_is_dst is False else 'src'

    stdout, stderr = _tc_execute_cmd(TC_FILTER, TC_ADD, TC_DEV, iface, TC_PARNT, prnt_qdisc_id,
                                     TC_PROT, TC_IP, TC_PRIO, "1", "u32", TC_FLOWID, prnt_class_id,
                                    "match", TC_IP, origin, ip)
    return


def tc_create_netem_qdisc(iface, ip, netem_def, qdisc_id, prnt_qdisc_id):
    stdout, stderr = _tc_execute_cmd(TC_QDISC, TC_ADD, TC_DEV, iface, TC_PARNT, prnt_qdisc_id,
                                     TC_HNDL, qdisc_id + ":", TC_NETEM, *netem_def.split(" "))
    return


def tc_change_netem_qdisc(iface, ip, netem_def, qdisc_id, prnt_qdisc_id):
    stdout, stderr = _tc_execute_cmd(TC_QDISC, TC_CHANGE, TC_DEV, iface, TC_PARNT, prnt_qdisc_id,
                                     TC_HNDL, qdisc_id + ":", TC_NETEM, *netem_def.split(" "))
    return

def debug_tc_showqdiscs():
    stdout, stderr = _tc_execute_cmd(TC_QDISC)
    log_raw_output(stdout, stderr)
