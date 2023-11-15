from importlib import import_module
import pkgutil
from pathlib import Path
import os
MODULE_PATH = os.path.dirname(os.path.realpath(__file__))

#print(MODULE_PATH)


__cls_cache = dict()

def factory(name: str, **kwargs):
    name = name + '_tester'
    mod = import_module('.' + name, package='tester')
    tester_cls = getattr(mod, name)
    instance = tester_cls(**kwargs)
    return instance


def factory_cls(name: str, **kwargs):
    name = str(name) + '_tester'
    if name in __cls_cache:
        return __cls_cache[name]
    else:
        mod = import_module('.' + name, package='tester')
        tester_cls = getattr(mod, name)
        __cls_cache[name] = tester_cls
        return tester_cls


def analyse_artifacts(tool_name: str, path: Path, apk_filename: str):
    tester_cls = factory_cls(tool_name)
    return tester_cls.analyse_artifacts(path, apk_filename)


def check_success(tool_name: str, path: Path, apk_filename: str):
    tester_cls = factory_cls(tool_name)
    return tester_cls.check_success(path, apk_filename)


def get_all_testers():
    tmp = []
    for importer, modname, ispkg in pkgutil.iter_modules([MODULE_PATH]):
        if (ispkg is False) and ('abstract' not in modname) and ('_tester' in modname):
            tmp.append(modname)
    return tmp
