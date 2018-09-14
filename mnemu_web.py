# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import json

from flask import Flask
from flask import request

import mnemu
from ip_filter import NetemType
from mnemu_presets import MNemuPresets

app = Flask(__name__, static_folder='web_content')
mnemu_web = None
mnemu_presets = MNemuPresets()

def get_ip(req):
    if "ip" in req.args.keys():
        ret_val = req.args.get("ip")
    else:
        ret_val = str(req.remote_addr)

    return ret_val


@app.route('/refreshrules')
def refresh_rules():
    mnemu_web.refresh_tc()
    return "true"

# region NETEM SET VALUES

@app.route('/<ipnum>/bandwidth/<val>/<inorout>')
def set_ip_bandwidth(ipnum, val, inorout):
    if inorout == "in":
        inbound = True
    else:
        inbound = False
    val_set_to = mnemu_web.set_ip_bandwidth(ipnum, val, inbound)
    return val_set_to


@app.route('/netem/set/<ipnum>')
def set_netem_value(ipnum):

    netem_type = request.args.get("netem_type")
    netem_val = request.args.get("netem_val")
    inbound = not request.args.__contains__("outbound")

    return mnemu_web.set_netem_setting_value(ipnum, netem_type, netem_val, inbound)


@app.route('/netem/set/corr/')
def set_netem_correlation():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    netem_corr = request.args.get("netem_corr")
    inbound = not request.args.keys().__contains__("outbound")

    return mnemu_web.set_netem_setting_corr(ip, netem_type, netem_corr, inbound)


# endregion NETEM SET VALUES

# region NETEM GET VALUES

@app.route('/netem/get/')
def get_netem_value():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    inbound = not request.args.keys().__contains__("outbound")

    return mnemu_web.get_netem_setting_value(ip, netem_type, inbound)


@app.route('/netem/get/corr/')
def get_netem_correlation():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    inbound = not request.args.keys().__contains__("outbound")

    return mnemu_web.get_netem_setting_corr(ip, netem_type, inbound)


# endregion NETEM GET VALUEs


@app.route('/ips/get')
def get_known_ips():
    ip_list = mnemu_web.get_known_ips()
    ip_list.sort()
    return json.dumps(ip_list)

@app.route('/me')
def setup_visitng_up():
    ip = get_ip(request)
    ret_val = {}
    ret_val["ip"] = ip
    ret_val["ip_data"] = mnemu_web.get_ip_settings(ip).as_dict();
    return json.dumps(ret_val)

@app.route('/ip/<ipnum>/clear')
def clear_ip_rules(ipnum):
    mnemu_web.clear_ip_rules(ipnum)
    return "true"

@app.route('/ip/<ipnum>/preset/<presetid>/<inorout>')
def set_ip_to_preset(ipnum, presetid, inorout):
    preset = mnemu_presets.get_preset(presetid)
    if preset is not None:
        inbound = True if inorout == "in" else False
        mnemu_web.set_netem_setting_from_preset(ipnum, preset, inbound)
        return 'true'
    else:
        return 'false'

@app.route('/ip/<ipnum>')
def specific_ip(ipnum):
    return mnemu_web.get_ip_settings(ipnum).web_str()

@app.route("/presets/get")
def get_presets():
    return json.dumps(mnemu_presets.get_preset_names())

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/test')
def test():
    ipsettings = mnemu_web.add_new_ip("192.168.1.1")
    ipsettings.set_in_rate("100")
    ipsettings.set_out_rate("100")
    ipsettings.set_netem_setting(NetemType.JITTER, 100)
    ipsettings.set_netem_setting(NetemType.JITTER, 100, False)
    ipsettings.set_netem_setting(NetemType.LATENCY, 100)
    ipsettings.set_netem_setting(NetemType.LATENCY, 100, False)

    return ipsettings.get_netem_inbound_cmd() + ipsettings.web_str()


if __name__ == '__main__':
    mnemu_web = mnemu.MNemu("ens192")
    app.run(host="0.0.0.0", port=9999)
