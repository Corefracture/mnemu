# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import json
import argparse
from flask import Flask
from flask import request
from mnemu.mnemu import MNemu
from mnemu.mnemu_presets import MNemuPresets

web_srv = Flask(__name__, static_folder='web_content')
mnemu_web = None
mnemu_presets = MNemuPresets()

def get_ip(req):
    if "ip" in req.args.keys():
        ret_val = req.args.get("ip")
    else:
        ret_val = str(req.remote_addr)
    return ret_val


# region FINAL REST API

# region IP OPERATIONS

# region IP CONFIGS SETTERS


@web_srv.route('/<ipnum>/bandwidth/set/<val>/<inorout>')
def set_ip_bandwidth(ipnum, val, inorout):
    inbound = inorout == "in"
    val_set_to = mnemu_web.set_ip_bandwidth(ipnum, val, inbound)
    return val_set_to


@web_srv.route('/<ipnum>/netem/set/<netem_type>/<netem_val>/<inorout>')
def set_netem_value(ipnum, netem_type, netem_val, inorout):
    inbound = inorout == "in"
    return mnemu_web.set_netem_setting_value(ipnum, netem_type, netem_val, inbound)


@web_srv.route('/<ipnum>/corr/set/<netem_type>/<corr_val>/<inorout>')
def set_netem_corr_value(ipnum, netem_type, corr_val, inorout):
    inbound = inorout == "in"
    return mnemu_web.set_netem_setting_corr(ipnum, netem_type, corr_val, inbound)


# endregion IP CONFIGS SETTERS


# region IP CONFIGS GETTTERS

@web_srv.route('/<ipnum>/bandwidth/get/<val>/<inorout>')
def get_ip_bandwidth(ipnum, val, inorout):
    inbound = inorout == "in"
    return mnemu_web.get_ip_bandwidth(ipnum, inbound)


@web_srv.route('/<ipnum>/netem/get/<netem_type>/<inorout>')
def get_netem_value(ipnum, netem_type, inorout):
    inbound = inorout == "in"
    return mnemu_web.get_netem_setting_value(ipnum, netem_type, inbound)


@web_srv.route('/<ipnum>/corr/get/<netem_type>/<inorout>')
def get_netem_corr_value(ipnum, netem_type, inorout):
    inbound = inorout == "in"
    return mnemu_web.get_netem_setting_corr(ipnum, netem_type, inbound)


# endregion IP CONFIGS GETTERS

@web_srv.route('/<ipnum>/clear')
def clear_ip_rules(ipnum):
    mnemu_web.clear_ip_rules(ipnum)
    return "true"


@web_srv.route('/<ipnum>/preset/<presetid>/<inorout>')
def set_ip_to_preset(ipnum, presetid, inorout):
    inbound = True if inorout == "in" else False
    preset = mnemu_presets.get_preset(presetid) \
        if inbound else mnemu_presets.get_preset(presetid, True)

    if preset is not None:
        mnemu_web.set_netem_setting_from_preset(ipnum, preset, inbound)
        return 'true'
    else:
        return 'false'


@web_srv.route('/<ipnum>/ignore')
def ignore_ip(ipnum):
    mnemu_web.ignore_ip(ipnum)
    return "true"


@web_srv.route('/<ipnum>/unignore')
def unignore_ip(ipnum):
    mnemu_web.unignore_ip(ipnum)
    return "true"


# endregion IP OPERATIONS

@web_srv.route('/ips/get')
def get_known_ips():
    ip_list = mnemu_web.get_known_ips()
    ip_list.sort()
    return json.dumps(ip_list)


@web_srv.route('/ips/ignored')
def get_ignored():
    return json.dumps(mnemu_web.ignored_ips)


@web_srv.route("/presets/get")
def get_presets():
    names = {
        "in": mnemu_presets.get_preset_names(),
        "out": mnemu_presets.get_preset_names(True)
    }
    return json.dumps(names)


@web_srv.route('/<ipnum>/add')
def specific_ip(ipnum):
    if ipnum not in mnemu_web.ignored_ips:
        return json.dumps(mnemu_web.get_ip_settings(ipnum).dict())
    else:
        return "{}"


@web_srv.route('/me')
def setup_visitng_up():
    ip = get_ip(request)
    ret_val = {"ip": ip}
    if ip not in mnemu_web.ignored_ips:
        ret_val["ip_data"] = mnemu_web.get_ip_settings(ip).dict()
    return json.dumps(ret_val)


@web_srv.route('/refreshrules')
def refresh_rules():
    mnemu_web.refresh_tc()
    return "true"


# endregion FINAL REST API


# region OLD REST API

@web_srv.route('/<ipnum>/bandwidth/<val>/<inorout>')
def set_ip_bandwidth_old(ipnum, val, inorout):
    if inorout == "in":
        inbound = True
    else:
        inbound = False
    val_set_to = mnemu_web.set_ip_bandwidth(ipnum, val, inbound)
    return val_set_to


@web_srv.route('/netem/set/<ipnum>')
def set_netem_value_old(ipnum):

    netem_type = request.args.get("netem_type")
    netem_val = request.args.get("netem_val")
    inbound = not request.args.__contains__("outbound")

    return mnemu_web.set_netem_setting_value(ipnum, netem_type, netem_val, inbound)


@web_srv.route('/netem/set/corr/')
def set_netem_correlation_old():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    netem_corr = request.args.get("netem_corr")
    inbound = not request.args.keys().__contains__("outbound")
    return mnemu_web.set_netem_setting_corr(ip, netem_type, netem_corr, inbound)


@web_srv.route('/netem/get/')
def get_netem_value_old():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    inbound = not request.args.keys().__contains__("outbound")
    return mnemu_web.get_netem_setting_value(ip, netem_type, inbound)


@web_srv.route('/netem/get/corr/')
def get_netem_correlation_old():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    inbound = not request.args.keys().__contains__("outbound")
    return mnemu_web.get_netem_setting_corr(ip, netem_type, inbound)


@web_srv.route('/ip/<ipnum>/ignore')
def ignore_ip_old(ipnum):
    mnemu_web.ignore_ip(ipnum)
    return "true"


@web_srv.route('/ignored')
def get_ignored_old():
    return json.dumps(mnemu_web.ignored_ips)


@web_srv.route('/ip/<ipnum>/unignore')
def unignore_ip_old(ipnum):
    mnemu_web.unignore_ip(ipnum)
    return "true"


@web_srv.route('/ip/<ipnum>/clear')
def clear_ip_rules_old(ipnum):
    mnemu_web.clear_ip_rules(ipnum)
    return "true"


@web_srv.route('/ip/<ipnum>/preset/<presetid>/<inorout>')
def set_ip_to_preset_old(ipnum, presetid, inorout):
    inbound = True if inorout == "in" else False
    preset = mnemu_presets.get_preset(presetid) \
        if inbound else mnemu_presets.get_preset(presetid, True)

    if preset is not None:
        mnemu_web.set_netem_setting_from_preset(ipnum, preset, inbound)
        return 'true'
    else:
        return 'false'


@web_srv.route('/ip/<ipnum>')
def specific_ip_old(ipnum):
    if ipnum not in mnemu_web.ignored_ips:
        return json.dumps(mnemu_web.get_ip_settings(ipnum).dict())
    else:
        return "{}"


# endregion OLD REST API

@web_srv.route('/')
def web_app():
    return web_srv.send_static_file('index.html')

def parse_args():
    args = argparse.ArgumentParser(description="Launches the web app and REST API for MNemu")
    args.add_argument("--ip", help="The IP Address to bind the web server to", required=True)
    args.add_argument("--port", help="The port number to bind too. Defaults to 80", required=False, type=int)
    args.add_argument("--iface", help="The network interface name to perform network emulation commands "
                                      "on", required=True)
    return args.parse_args()

if __name__ == '__main__':
    arg_vals = parse_args()
    mnemu_web = MNemu(arg_vals.iface)
    web_srv.run(host=arg_vals.ip, port=arg_vals.port)
