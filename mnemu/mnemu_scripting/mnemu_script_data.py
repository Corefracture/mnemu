# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details


import time
import json


class MNemuScriptRuleSetting:
    def __init__(self, base_val=None, high_val=None, random_update=None, update_prob=None,
                 active_prob=None, setting_type=None, repeats=None, json_data_load=None):
        if json_data_load is None:
            self.base_val = base_val
            self.high_val = high_val
            self.random_update = random_update
            self.update_prob = update_prob
            self.active_prob = active_prob
            self.setting_type = setting_type
            self.repeats = repeats
        else:
            self.__dict__ = json_data_load


class MNemuScriptRuleTiming:
    def __init__(self, start_secs=None, end_secs=None, active_dur_secs=None, repeat_delay_secs=None,
                 repeat_count=None, active_dir_rnd_inc=None, eval_interval=None, json_data_load=None):
        if json_data_load is None:
            self.start_secs = start_secs
            self.end_secs = end_secs
            self.active_dur_secs = active_dur_secs
            self.active_dur_rnd_inc = active_dir_rnd_inc
            self.repeat_delay_secs = repeat_delay_secs
            self.repeat_count = repeat_count
            self.eval_interval = eval_interval
        else:
            self.__dict__ = json_data_load

        return


class MNemuScriptRule:
    def __init__(self, rule_setting=None, rule_timing=None, json_settings=None, json_timings=None):
        if json_settings is not None and \
                json_timings is not None:
            self._load_from_json(json_settings, json_timings)
        else:
            self.setting = rule_setting
            self.timing = rule_timing
        return

    def _load_from_json(self, setting, timing):
        self.setting = MNemuScriptRuleSetting(json_data_load=json.loads(setting))
        self.timing = MNemuScriptRuleTiming(json_data_load=json.loads(timing))
        return

    def to_dicts(self):
        rule_setting = self.setting.__dict__
        rule_timing = self.timing.__dict__
        return rule_setting, rule_timing


class MNemuRuleInstState:
    def __init__(self, original_val, rule_id):
        now = time.time()
        self.original_val = original_val
        self.rule_id = rule_id
        self.current_val = self.original_val
        self.last_deactivate = now
        self.last_activate = now
        self.activated_times = 0
        self.start_time = now
        self.is_active = False
        self.last_eval = now
        self.is_done = False


class MNemuScriptInstState:
    def __init__(self, script_id, ip, ip_settings, inbound = True):
        self.rule_states = []
        self.script_id = script_id
        self.pending_removal = False
        self.ip = ip
        self.ip_settings = ip_settings
        self.inbound = inbound
        return









