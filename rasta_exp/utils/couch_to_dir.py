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


db_name = sys.argv[1]
dir_name = sys.argv[2]

couch_db = couch_srv['rasta-' + db_name]

if os.path.isdir(dir_name):
    raise Exception(f"Path {dir_name} already exists. Aborting")

os.makedirs(dir_name)

for uid in couch_db:
    (sha, task) = uid.split('_-_')
    report = couch_db[uid]
    with open(os.path.join(dir_name, uid), 'w') as f_out:
        json.dump(report, f_out)

