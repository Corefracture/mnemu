
from mnemu.mnemu_scripting.mnemu_script import *

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

