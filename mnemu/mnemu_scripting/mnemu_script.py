# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import json
import random

from mnemu.mnemu_scripting.mnemu_script_data import *


class MNemuScript:
    def __init__(self, mnemu_inst, script_id =-1, json_data_str=None):
        self._instances = []
        self._repeats = False
        self._rules = []
        self._name = ""
        self._tags = []
        self._id = script_id
        self._mnemu_inst = mnemu_inst

        if json_data_str is not None:
            self._load_from_json(json_data_str)

    def _load_from_json(self, json_data_str):
        saved = json.loads(json_data_str)
        self._repeats = saved["repeats"]
        self._name = saved["name"]
        self._tags = saved["tags"]

        rules_data_raw = json.loads(saved["rules"])
        self._rules = []
        for rule in rules_data_raw:
            self._rules.append(MNemuScriptRule(rule['setting'], rule['timing']))
        return

    def init_new_script_inst(self, script_id, ip, ip_settings, inbound=True):
        script_inst = MNemuScriptInstState(script_id, ip, ip_settings, inbound)
        for x in range(0, len(self._rules)):
            rule_setting = self._rules[x].setting
            orig_val = ip_settings.get_netem_setting(rule_setting.setting_type, inbound)
            script_inst.rule_states.append(MNemuRuleInstState(orig_val, x))

        self._instances.append(script_inst)
        return script_inst

    def update(self):
        try:
            insts_to_rem = []
            for script_inst in self._instances:
                if script_inst.pending_removal:
                    insts_to_rem.append(script_inst)
                else:
                    self._update_rule_instances(script_inst)

            for inst_to_rem in insts_to_rem:
                self._instances.remove(inst_to_rem)
                inst_to_rem = None

        except Exception as exp:
            #TODO: cf: More logging and handling
            return

    def _update_rule_instances(self, script_inst):
        can_remove_script = True
        for rule_inst in script_inst.rule_states:
            if rule_inst.is_done is True:
                continue
            can_remove_script = False
            rule_def = self._rules[rule_inst.rule_id]
            if self._set_rule_done(rule_inst, rule_def) is True:
                self._set_setting_to_orig(rule_inst, rule_def.setting, script_inst)

            if rule_inst.is_active is True:
                if self._should_deactivate(rule_def.timing, rule_def.setting, rule_inst):
                    self._deactivate_rule(rule_inst)
                else:
                    self._eval_rule_and_update(rule_def.setting, rule_def.timing, script_inst, rule_inst)
            else:
                if self._should_activate_rule(rule_def.setting, rule_def.timing, rule_inst):
                    self._activate_rule(rule_inst)
                    self._eval_rule_and_update(rule_def.setting, rule_def.timing, script_inst, rule_inst)

        script_inst.pending_removal = can_remove_script
        return

    @staticmethod
    def _check_probability(rule_setting):
        return random.randrange(0, 100) < rule_setting.update_prob

    def _set_rule_done(self, rule_inst, rule_def):
        is_done = False
        if (time.time() - rule_inst.start_time) > rule_def.timing.end_secs:
            is_done = True
        if rule_def.setting.repeats is False:
            is_done = True
        else:
            if rule_inst.activated_times >= rule_def.timing.repeat_count:
                is_done = True

        rule_inst.is_done = is_done
        return is_done


    def _set_setting_to_orig(self, rule_inst, rule_setting, script_inst):
        self._mnemu_inst.set_netem_setting_value(script_inst.ip, rule_setting.setting_type, rule_inst.original_val,
                                                 script_inst.inbound)

    def _eval_rule_and_update(self, rule_setting, rule_timing, script_inst, rule_inst):
        now = time.time()
        if rule_setting.random_update is True and \
        ((now - rule_inst.last_eval) > rule_timing.eval_interval):
            if  MNemuScript._check_probability(rule_setting) is True:
                new_val = self._roll_new_val(rule_setting)
                rule_inst.current_val = new_val
                rule_inst.last_eval = now
                ip_setting = script_inst.ip_settings

                self._mnemu_inst.set_netem_setting_value(script_inst.ip, rule_setting.setting_type, new_val, script_inst.inbound)

                #ip_setting.set_netem_setting(rule_setting.setting_type, new_val, script_inst.inbound)

    def _deactivate_rule(self, rule_inst):
        rule_inst.is_active = False
        rule_inst.last_deactivate = time.time()


    def _should_deactivate(self, rule_timing, rule_setting, rule_inst):
        now = time.time()
        if (now - rule_inst.last_activate) > rule_timing.active_dur_secs:
            return True

        return False

    def _activate_rule(self, rule_inst):
        rule_inst.is_active = True
        rule_inst.last_activate = time.time()

    def _should_activate_rule(self, rule_setting, rule_timing, rule_inst):
        now = time.time()
        if (rule_inst.activated_times == 0) or \
            (rule_inst.activated_times > 0 and rule_setting.repeats is True):
            if (now - rule_inst.last_deactivate) > rule_timing.repeat_delay_secs:
                if random.randrange(0, 100) < rule_setting.active_prob:
                    return True

        return False

    def _roll_new_val(self, rule_setting):
        return random.randrange(rule_setting.base_val, rule_setting.high_val)

    def to_json(self):
        data = {}
        data["repeats"] = str(self._repeats)
        data["name"] = self._name
        data["tags"] = self._tags
        rules_data = []
        for rule in self._rules:
            setting, timing = rule.to_dicts()
            rules_data.append({"setting": setting, "timing": timing})
        data["rules"] = json.dumps(rules_data)

        return json.dumps(data)



#testing
