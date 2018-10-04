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
        self._rules = []
        self._repeats = False
        self._name = ""
        self._tags = []

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

    def update(self):
        try:
            for x in range(0, len(self._rule_states)):
                rule_state = self._rule_states[x]
                rule_setting = self._rule_settings[x]
                rule_timing = self._rule_timings[x]

        except Exception as exp:
            #TODO: cf: More logging and handling
            return

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

script = MNemuScript()
rule_setting = MNemuScriptRuleSetting(1,2,3,4,5,6)
rule_timing = MNemuScriptRuleTiming(10,20,30,40,50,60)
rule = MNemuScriptRule(rule_setting, rule_timing)
script._rules.append(rule)

rule_setting = MNemuScriptRuleSetting(10,20,30,40,50,60)
rule_timing = MNemuScriptRuleTiming(100,200,300,400,500,600)
rule2 = MNemuScriptRule(rule_setting, rule_timing)

script._rules.append(rule2)

json_str = script.to_json()

print(json_str)

new_script = MNemuScript(json_data_str=json_str)

if new_script is not None:
    print("Yay!")

