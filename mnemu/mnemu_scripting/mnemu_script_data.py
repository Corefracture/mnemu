# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details


import random
import time
import json


class MNemuScriptRuleSetting:
    def __init__(self, base_val=None, high_val=None, eval_interval=None, random_update=None,
                 update_prob=None, active_prob=None, json_data_load=None):
        if json_data_load is None:
            self._base_val = base_val
            self._high_val = high_val
            self._eval_interval = eval_interval
            self._random_update = random_update
            self._update_prob = update_prob
            self._active_prob = active_prob
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


class MNemuScriptRuleTiming:
    def __init__(self, start_secs=None, end_secs=None, active_dur_secs=None, repeat_delay_secs=None,
                 repeat_count=None, active_dir_rnd_inc=None, json_data_load=None):
        if json_data_load is None:
            self._start_secs = start_secs
            self._end_secs = end_secs
            self._active_dur_secs = active_dur_secs
            self._active_dur_rnd_inc = active_dir_rnd_inc
            self._repeat_delay_secs = repeat_delay_secs
            self._repeat_count = repeat_count
        else:
            self.__dict__ = json_data_load

        return

    def to_json(self):
        return json.dumps(self.__dict__)


class MNemuScriptRuleState:
    def __init__(self):
        self.current_val = 0
        self.last_activate = time.time()
        self.start_time = time.time()
        self.is_active = False
        self.last_eval = time.time()
        return
