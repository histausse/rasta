#!/usr/bin/env python3


import couchdb
import json
import sys
import os
import configparser
_config = configparser.ConfigParser()
_config.read("settings.ini")
_cfg = _config["Couch"]
couch_srv = couchdb.Server(f"http://{_cfg.get('user')}:{_cfg.get('password')}@{_cfg.get('host')}:{_cfg.getint('port')}/")


set_name = sys.argv[1]

couch_db = couch_srv['rasta-' + set_name]

tools = set()
with open('tools', 'r') as f:
    for line in f.readlines():
        tools.add(line.strip())


set_size = 0
with open(f'dataset/{set_name}', 'r') as f:
    set_size = len(f.readlines())

task_num = set_size * len(tools)
results = dict()
for tool in tools:
    results[tool] = {'FINISHED': 0, 'TIMEOUT': 0, 'FAILED': 0, 'UNKNOWN': 0, 'MISSING': 0} 

for uid in couch_db:
    (sha, tool) = uid.split('_-_')

    report = couch_db[uid]
    results[tool][report['tool-status']] += 1
#    if report and 'tool-status' in report:
#        if report['tool-status'] == 'FINISHED':
#            print(uid)

global_res = {'FINISHED': 0, 'TIMEOUT': 0, 'FAILED': 0, 'UNKNOWN': 0, 'MISSING': 0} 
for tool in sorted(list(tools)):
    results[tool]['MISSING'] = set_size - results[tool]['FINISHED'] -  results[tool]['FAILED'] -  results[tool]['TIMEOUT'] -  results[tool]['UNKNOWN']
    for status in ['FINISHED', 'TIMEOUT', 'FAILED', 'UNKNOWN', 'MISSING']:
        results[tool][f"{status}_rate"] = (results[tool][status] * 100) / set_size
        global_res[status] += results[tool][status]

for status in ['FINISHED', 'TIMEOUT', 'FAILED', 'UNKNOWN', 'MISSING']:
    global_res[f"{status}_rate"] = (global_res[status] * 100) / task_num


print(';'.join( [set_name] + sorted(list(tools)) + ['TOTAL']) )
for status in ['FINISHED', 'FAILED', 'TIMEOUT', 'UNKNOWN', 'MISSING', 'FINISHED_rate', 'FAILED_rate', 'TIMEOUT_rate', 'UNKNOWN_rate', 'MISSING_rate']:
    _tmp_row = []
    _tmp_row.append(status)
    for tool in sorted(list(tools)):
        _tmp = results[tool][status]
        if status.endswith('rate'):
            _tmp_row.append(f"{_tmp:.2f}")
        else:
            _tmp_row.append(f"{_tmp}")
    if status.endswith('rate'):
        _tmp_row.append(f"{global_res[status]:.2f}")
    else:
        _tmp_row.append(f"{global_res[status]}")
    print(";".join(_tmp_row))

#print(results)
#print(global_res)
