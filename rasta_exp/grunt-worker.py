#!/usr/bin/env python3

import requests
import os
import sys
import uuid
import shutil
import argparse
import configparser
import time
import subprocess
from pathlib import Path
import tester
import json


# - Get jobs
# - Create tmp dir
# - Get APK
# - launch container
# - get results
# - store results


def get_settings() -> configparser.ConfigParser:
    _config = configparser.ConfigParser()
    _config.read("settings.ini")
    if "AndroZoo" not in _config.sections():
        raise Exception("settings needs a 'AndroZoo' section")
    apikey = _config["AndroZoo"].get("apikey", None)
    if (not apikey) or (len(apikey) != 64):
        raise Exception("Invalid AndroZoo apikey")
    return _config


def get_apk_from_androzoo(
    sha256: str, apikey: str, base_url=None, reraise=False, local_cache=None
):
    if len(sha256) != 64:
        print("Not a sha256, failure disabled for tests")
        # return None
    if not base_url:
        base_url = "https://androzoo.uni.lu"
    if local_cache is not None and not Path(local_cache).exists():
        print("Error: local cache not available: " + str(local_cache))
    if local_cache is not None and (Path(local_cache) / f"{sha256}").exists():
        with (Path(local_cache) / f"{sha256}").open("rb") as file:
            data = file.read()
        return data
    if (
        local_cache is not None
        and (Path(local_cache) / f"{sha256.upper()}.apk").exists()
    ):
        with (Path(local_cache) / f"{sha256.upper()}.apk").open("rb") as file:
            data = file.read()
        return data
    try:
        url = f"{base_url}/api/download?apikey={apikey}&sha256={sha256}"
        r = requests.get(url, timeout=600)
        if r.status_code == 200:
            return r.content
        else:
            print(f"get_apk_from_androzoo: NOT 200: {str(r.status_code)}")
            return None
    except Exception as e:
        print(f"Failed to get APK from AndroZoo: {str(e)}")
        if reraise:
            raise
    return None


def get_unique_id(sha: str, task: str):
    return f"{sha}-_-{task}"


def save_to_couch(couch_db, uid: str, js: dict, overwrite=False):
    if uid in couch_db:
        if overwrite is True:
            _doc = couch_db[uid]
            couch_db.delete(_doc)
            couch_db[uid] = js
        else:  # NO overwrite
            pass
    else:
        couch_db[uid] = js
    return


def mark_done(redis_srv, redis_prefix, uid: str):
    redis_srv.sadd(f"{redis_prefix}:DONE", uid)
    return


def is_already_done(redis_srv, redis_prefix, uid: str):
    redis_srv.sismember(f"{redis_prefix}:DONE", uid)
    return


def do_one_job(
    sha256: str,
    tool_name: str,
    base_dir: str,
    apk_blob,
    container_mode,
    container_image,
    keep_tmp_dir=False,
):
    # create unique dir in basedir
    _uuid = str(uuid.uuid4())
    _dir = os.path.join(base_dir, _uuid)
    if os.path.isdir(_dir):
        shutil.rmtree(_dir)
    os.makedirs(_dir)
    _work_dir = os.path.join(_dir, "work")
    os.makedirs(_work_dir)
    _tmp_dir = os.path.join(_dir, "tmp")
    os.makedirs(_tmp_dir)
    try:
        # save apk_blob to disk
        with open(os.path.join(_work_dir, sha256 + ".apk"), "wb") as f_out:
            f_out.write(apk_blob)
        # launch-container.sh MODE TOOL_NAME CONTAINER_IMG WORKDIR TMP_DIR APK_FILENAME
        exec_res = subprocess.run(
            [
                "./launch-container.sh",
                container_mode,
                tool_name,
                container_image,
                _work_dir,
                _tmp_dir,
                sha256 + ".apk",
            ]
        )
        result = tester.analyse_artifacts(
            tool_name=tool_name, path=Path(_work_dir), apk_filename=sha256 + ".apk"
        )

    finally:
        if keep_tmp_dir is False:
            if os.path.isdir(_dir):
                shutil.rmtree(_dir)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-dir",
        help="Location of the base dir to run the experiment",
        default=None,
        type=str,
        action="store",
    )
    parser.add_argument(
        "--result-dir",
        help="Location of the dir to store the results if --no-write-to-couch is set",
        default=None,
        type=str,
        action="store",
    )
    parser.add_argument(
        "--keep-tmp-dir",
        help="Do not remove the tmp directory created",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--overwrite",
        help="Overwrite results in CouchDB",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--no-mark-done",
        help="Do not mark apps as DONE in REDIS",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--no-write-to-couch",
        help="Do not write results in CouchDB",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--redo",
        help="Redo even if already marked as DONE in REDIS",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--manual",
        help="[debug] Process the sha256 in parameters instead of getting sha256 TODO from REDIS.",
        default=False,
        action="store_const",
        const=True,
    )
    parser.add_argument(
        "--task", help="[debug] Name of the task to perform", type=str, action="store"
    )
    parser.add_argument(
        "--sha", help="[debug] sha to make the --task on", type=str, action="store"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--docker", action="store_true")
    group.add_argument("--singularity", action="store_true")
    parser.add_argument(
        "--image-basedir",
        help="Base dir for Singularity images",
        type=str,
        action="store",
        default=None,
    )

    args = parser.parse_args()
    base_dir = args.base_dir
    if base_dir is None:
        base_dir = "/tmp/"
    result_dir = args.result_dir
    if result_dir is None:
        result_dir = base_dir
    
    # base_dir = os.path.join(base_dir, str(uuid.uuid4()))
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)
    _need_couch = True
    if args.no_write_to_couch:
        _need_couch = False
    _need_redis = True
    if args.manual:
        _need_redis = False
    _config = get_settings()
    _cfg = _config["AndroZoo"]
    androzoo_apikey = _cfg.get("apikey")
    androzoo_base_url = _cfg.get("base_url")  # optional
    androzoo_local_cache = _cfg.get("local_cache")  # optional
    redis_srv = None
    redis_prefix = None
    if _need_redis:
        if "Redis" not in _config.sections():
            raise Exception("settings needs a 'Redis' section")
        _cfg = _config["Redis"]
        import redis

        redis_prefix = _cfg.get("prefix")
        redis_srv = redis.Redis(
            host=_cfg.get("host"),
            port=_cfg.getint("port"),
            db=_cfg.getint("db"),
            password=_cfg.get("password"),
        )
        if redis_srv is None:
            raise Exception("Was unable to connect to redis. Exiting")
    # print("Need redis: " f"{_need_redis}")
    couch_srv = None
    couch_db = None
    if _need_couch:
        if "Couch" not in _config.sections():
            raise Exception("settings needs a 'Couch' section")
        import couchdb

        _cfg = _config["Couch"]
        couch_srv = couchdb.Server(
            f"http://{_cfg.get('user')}:{_cfg.get('password')}@{_cfg.get('host')}:{_cfg.getint('port')}/"
        )
        couch_db = couch_srv[_cfg.get("db")]

    # Docker or Singularity?
    if args.singularity:
        if args.image_basedir is None:
            raise Exception(
                "When using --singularity, --image-basedir MUST be provided"
            )

    _container_mode = None
    if args.singularity:
        _container_mode = "SINGULARITY"
    elif args.docker:
        _container_mode = "DOCKER"
    #        raise NotImplementedError(
    #            "*** DOCKER DEACTIVATED ***\nToo many problems with docker. We'll focus on singularity only"
    #        )
    assert _container_mode != None

    def get_container_image_name(tool_name: str):
        # If SINGULARITY, we need to  return the path to the sif file (without the trailing .sif)
        if _container_mode == "SINGULARITY":
            return os.path.join(args.image_basedir, "rasta-" + tool_name)
        else:
            # Docker
            return "rasta-" + tool_name

    # MODE 1 : DEBUG / Manual
    if args.manual:
        if (args.task is None) or (args.sha is None):
            raise Exception("Debug mode must be used with BOTH --task and --sha")
        task = args.task
        # sha = str(args.sha).upper() # TMP patch
        sha = str(args.sha)
        if len(sha) != 64:
            # raise Exception("invalid --sha value")
            print("invalid --sha value, exception disabled for tests")
        apk_blob = get_apk_from_androzoo(
            sha256=sha,
            apikey=androzoo_apikey,
            base_url=androzoo_base_url,
            reraise=False,
            local_cache=androzoo_local_cache,
        )
        if apk_blob is None:
            print(f"Unable to obtain apk for sha={sha}")
        else:
            # do_one_job(sha256: str, tool_name: str, base_dir: str, apk_blob, container_mode, container_image, keep_tmp_dir=False):
            res = do_one_job(
                sha256=sha,
                tool_name=task,
                base_dir=base_dir,
                apk_blob=apk_blob,
                container_mode=_container_mode,
                container_image=get_container_image_name(task),
                keep_tmp_dir=args.keep_tmp_dir,
            )
            # Debug / manual mode => will not mark the task as done in redis
            if res:
                if args.no_write_to_couch is False:
                    save_to_couch(
                        couch_db=couch_db,
                        uid=get_unique_id(sha=sha, task=task),
                        js=res,
                        overwrite=args.overwrite,
                    )
                else:
                    print(f"RESULT for task={task}, apk sha={sha}:\n{res}")
                    with open(str(result_dir) + f"/{sha}_-_{task}.json", "w") as f:
                        json.dump(res, f)
        # jobs is done, exiting
        sys.exit()

    # Normal Mode : grunt    loop read_task_from_redis, do_task, store_result
    while True:
        uid = redis_srv.spop(f"{redis_prefix}:TODO")
        if uid is None:
            print("got none")
            print("No more jobs in the queue. Aborting")
            sys.exit(111)
        uid = uid.decode("utf-8")
        (sha, task) = uid.split("_-_")
        if args.redo:
            pass  # no need to check if this task is already done else:
        else:
            if (
                (uid in couch_db)
                and ("tool-status" in couch_db[uid])
                and (couch_db[uid]["tool-status"] == "FINISHED")
            ):
                # if redis_srv.sismember(f"{redis_prefix}:DONE", uid):
                print(f"Already done, skipping. sha={sha}, task={task}")
                continue

        if len(sha) != 64:
            print(f"invalid sha from redis sha={sha}, task={task}")
            continue
        print(f"Got a task from redis: sha={sha}, task={task}")
        sha = sha.upper()
        apk_blob = get_apk_from_androzoo(
            sha256=sha,
            apikey=androzoo_apikey,
            base_url=androzoo_base_url,
            reraise=False,
            local_cache=androzoo_local_cache,
        )
        if apk_blob is None:
            print(f"Unable to obtain apk for sha={sha}")
            continue
        sys.stdout.flush()
        res = do_one_job(
            sha256=sha,
            tool_name=task,
            base_dir=base_dir,
            apk_blob=apk_blob,
            container_mode=_container_mode,
            container_image=get_container_image_name(task),
            keep_tmp_dir=args.keep_tmp_dir,
        )
        if res:
            if args.no_write_to_couch is False:
                save_to_couch(
                    couch_db=couch_db, uid=uid, js=res, overwrite=args.overwrite
                )
            if args.no_mark_done is False:
                if res["tool-status"] == "FINISHED":  # TODO:
                    mark_done(redis_srv=redis_srv, redis_prefix=redis_prefix, uid=uid)
        sys.exit(0)
