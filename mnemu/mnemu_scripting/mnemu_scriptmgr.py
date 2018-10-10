# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import time
from threading import Lock
from .mnemu_script_data import MNemuScriptInstState
from .mnemu_script import MNemuScript
from .mnemu_script_data import MNemuScriptRuleSetting, MNemuScriptRuleTiming, MNemuScriptRule
from mnemu.netem_defs import NetemType

class MNemuScriptMgr:
    def __init__(self, mnemu_inst, update_delay_s):
        self._master_scripts = {}
        self._ips_script_map = {}
        self._update_delay_s = update_delay_s
        self._last_update = time.time()
        self._locker = Lock()
        self._mnemu = mnemu_inst

        script = MNemuScript(mnemu_inst, 1)
        rule_setting = MNemuScriptRuleSetting(1000, 2000, True, 100, 100, "2", True)
        rule_timing = MNemuScriptRuleTiming(5, 30, 5, 2, 500, None, 5)
        rule = MNemuScriptRule(rule_setting, rule_timing)
        script._rules.append(rule)

        self._master_scripts[1] = script


    def update(self):
        while(True):
            if(time.time() - self._last_update) < self._update_delay_s:
                time.sleep(1)
                continue


            for id, script in self._master_scripts.items():
                script.update()

            self._locker.acquire()
            to_rem = []
            for ip, scripts in self._ips_script_map.items():
                if scripts["in"] is None:
                    self.remove_script_from_ip(ip, True)
                if scripts["out"] is None:
                    self.remove_script_from_ip(ip, False)

                if scripts["in"] is None and scripts["out"] is None:
                    to_rem.append(ip)

            for ip in to_rem:
                del self._ips_script_map[ip]
            self._locker.release()

            self._last_update = time.time()
        return

    #TODO: cf: more robust script removal that resets the all rule types to original val
    def remove_script_from_ip(self, ip, inbound=True):
        index = "in" if inbound is True else "out"
        if ip in self._ips_script_map:
            ip_scripts = self._ips_script_map[ip]
            if ip_scripts[index] is not None:
                ip_scripts[index].pending_removal = True
        return

    def set_script_on_ip(self, ip, ip_settings, script_id, inbound=True):
        in_or_out = "in" if inbound is True else "out"
        if ip not in self._ips_script_map:
            self._ips_script_map[ip] = {"in":None, "out":None}

        #Remove / flag any existing running script to be removed
        ip_script_state = self._ips_script_map[ip][in_or_out]
        if ip_script_state is not None:
            ip_script_state.pending_removal = True

        #Initialize a new instance of the script and assign to that ip
        base_script = self._master_scripts[script_id]
        self._ips_script_map[ip][in_or_out] = \
            base_script.init_new_script_inst(script_id, ip, ip_settings, inbound)
        return








