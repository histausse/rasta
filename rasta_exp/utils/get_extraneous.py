#!/usr/bin/env python3
#
# Just to check that no report ended up in the wrong DB

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

todo = set()
with open(f"{set_name}_all", 'r') as f_in:
    for line in f_in.readlines():
        todo.add(line.strip())


for uid in couch_db:
    #(sha, task) = uid.split('_-_')
    if uid in todo:
        continue
    else:
        print(uid)

