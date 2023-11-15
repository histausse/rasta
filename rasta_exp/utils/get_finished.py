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

couch_db = couch_srv[db_name]


for uid in couch_db:
    (sha, task) = uid.split('_-_')
    report = couch_db[uid]
    if report and 'tool-status' in report:
        if report['tool-status'] == 'FINISHED':
            print(uid)

