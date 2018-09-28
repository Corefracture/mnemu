# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import json
import random
import time


class MNemuScriptRuleSetting:
    def __init__(self, base_val=None, high_val=None, eval_interval=None, random_update=None,
                 update_prob=None, json_data_load=None):
        if json_data_load is None:
            self._base_val = base_val
            self._high_val = high_val
            self._eval_interval = eval_interval
            self._random_update = random_update
            self._update_prob = update_prob
        else:
            self.__dict__ = json_data_load

    def _update_val(self):
        return random.randrange(self._base_val, self._high_val)

    def _check_probability(self):
        return random.random() < self._update_prob

    def _eval_and_update(self):
        was_updated = False
        now = time.time()
        if self._random_update is True and \
                ((now - self._last_update) > self._eval_interval):
            if self._check_probability() is True:
                was_updated = True
                self._update_val()
                self._last_update = now
        return was_updated

    def force_update_and_get(self):
        return self._update_val()

    def get_val(self):
        should_update = self._eval_and_update()
        return should_update, self._update_val()

    def to_json(self):
        return json.dumps(self.__dict__)


class MNemuRuleTiming:
    def __init__(self):
        return

    def to_json(self):
        return json.dumps(self.__dict__)


class MNemuScript:
    def __init__(self, json_data_str=None):
        self._rule_settings = []
        self._rule_timings = []
        self._repeats = False

        if json_data_str is not None:
            self._load_from_json(json_data_str)

    def _load_from_json(self, json_data_str):
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
