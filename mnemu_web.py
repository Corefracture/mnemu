import json

from flask import Flask
from flask import request

import mnemu
from ip_filter import NetemType

app = Flask(__name__, static_folder='web_content')
mnemu_web = None


def get_ip(req):
    ret_val = None
    if "ip" in req.args.keys():
        ret_val = req.args.get("ip")
    else:
        ret_val = str(req.remote_addr)

    return ret_val


# region NETEM SET VALUES

@app.route('/netem/set/')
def set_netem_value():
    ip = get_ip(request)
    netem_type = request.args.get("netem_type")
    netem_val = request.args.get("netem_val")
    inbound = not request.args.keys().__contains__("outbound")

    return mnemu_web.set_netem_setting_value(ip, netem_type, netem_val, inbound)


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
    return json.dumps(mnemu_web.get_known_ips())


@app.route('/ip/<ipnum>')
def specific_ip(ipnum):
    return

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
    mnemu_web = mnemu.MNemu("none", '9999')
    app.run()
