# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import json

from mnemu.mnemu_scripting.mnemu_script_data import *


class MNemuScript:
    def __init__(self, json_data_str=None):
        self._rule_settings = []
        self._rule_timings = []
        self._rule_states = []
        self._repeats = False
        self._name = ""
        self._tags = []

        if json_data_str is not None:
            self._load_from_json(json_data_str)

    def _load_from_json(self, json_data_str):
        saved = json.loads(json_data_str)
        repeats = saved["repeats"]
        rules_data_raw = json.loads(saved["rules"])
        rules_timing_raw = json.loads(saved["timing"])
        if(len(rules_data_raw) != len(rules_timing_raw)):
            raise Exception("Rules data and rules timing do not match!")
            #TODO: cf: More logging and handeling here.
        self._rule_settings = []
        self._rule_timings = []
        for x in range(0, len(rules_data_raw)):
            self._rule_settings.append(
                MNemuScriptRuleSetting(json_data_load=json.loads(rules_data_raw[x])))
            self._rule_timings.append(
                MNemuScriptRuleTiming(json_data_load=json.loads(rules_timing_raw[x])))
        return

    def to_json(self):
        data = {}
        data["repeats"] = str(self._repeats)
        rule_data = []
        timing_data = []
        for rule in self._rule_settings:
            rule_data.append(rule.to_json())
        data["rules"] = json.dumps(rule_data)
        for timing in self._rule_timings:
            timing_data.append(timing.to_json())
        data["timing"] = json.dumps((timing_data))

        return json.dumps(data)
