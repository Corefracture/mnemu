# Copyright (C) 2018 Corefracture, Chris Coleman.
# www.corefracture.com - @corefracture
#
# Licensed under the MIT License, https://opensource.org/licenses/MIT
# See LICENSE.md for more details

import time


class MNemuScriptMgr:
    def __init__(self, update_delay_s):
        self._master_scripts = []
        self._script_instances = {}
        self._update_delay_s = update_delay_s
        self._last_update = time.time()

    def update(self):
        if(time.time() - self._last_update < self._update_delay_s):
            return

