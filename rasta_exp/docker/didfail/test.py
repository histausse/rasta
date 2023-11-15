import datetime
import importlib.util
import logging
import re

from typing import Any, Type, Optional
from pathlib import Path
from more_itertools import peekable


if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))

import orchestrator

errors = orchestrator.error_collector
utils = orchestrator.utils


TIMEOUT = 900


GUEST_MNT = "/mnt"
PATH_APK = f"{GUEST_MNT}/app.apk"

WORKDIR = "/"
CMD = "/workspace/run.sh"

TOOL_NAME = "didfail"

# Version name -> folder name
TOOL_VERSIONS = {
    "provided_build": "provided_build",
    "home_build": "home_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"

EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [errors.PythonError]

EXPECTED_ERROR_TYPES_FLOWDROID: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    errors.FlowdroidLog4jError,
]

EXPECTED_ERROR_TYPES_XFORM: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    errors.FlowdroidLog4jError,
]

EXPECTED_ERROR_TYPES_DARE: list[Type[errors.LoggedError]] = []


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = []
    flowdroid_log = path / "out" / "log" / "app.flowdroid.log"
    dare_log = path / "out" / "log" / "app.dare.log"
    xform_log = path / "out" / "log" / "app.xform.log"
    report["errors"].extend(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stdout", EXPECTED_ERROR_TYPES),
        )
    )
    if flowdroid_log.exists():
        report["errors"].extend(
            map(
                lambda e: e.get_dict(),
                errors.get_errors(flowdroid_log, EXPECTED_ERROR_TYPES_FLOWDROID),
            )
        )
    if dare_log.exists():
        report["errors"].extend(
            map(
                lambda e: e.get_dict(),
                errors.get_errors(dare_log, EXPECTED_ERROR_TYPES_DARE),
            )
        )
    if xform_log.exists():
        print
        report["errors"].extend(
            map(
                lambda e: e.get_dict(),
                errors.get_errors(xform_log, EXPECTED_ERROR_TYPES_XFORM),
            )
        )

    if report["timeout"]:
        report["tool-status"] = "TIMEOUT"
    elif check_success(path, report):
        report["tool-status"] = "FINISHED"
    else:
        report["tool-status"] = "FAILED"
    report["tool-name"] = TOOL_NAME
    report["date"] = str(datetime.datetime.now())
    report["apk"] = utils.sha256_sum(path / "app.apk").upper()
    return report


def check_success(path: Path, report: dict[str, Any]) -> bool:
    """Check if the analysis finished without crashing."""
    with (path / "stdout").open("r", errors="replace") as file:
        for line in file:
            if line == "Failure!\n":
                return False
    if report["exit-status"] != 0:
        return False
    flowfile = path / "out" / "flows.out"
    if not flowfile.exists():
        return False
    return flowfile.stat().st_size > 1


if __name__ == "__main__":
    import docker  # type: ignore

    args = orchestrator.get_test_args(TOOL_NAME)
    tool_folder = Path(__file__).resolve().parent
    api_key = orchestrator.get_androzoo_key()
    if args.get_apk_info:
        orchestrator.load_apk_info(args.apk_refs, args.androzoo_list, api_key)
    client = docker.from_env()

    logging.info("Command tested: ")
    logging.info(f"[{WORKDIR}]$ {CMD}")

    for apk_ref in args.apk_refs:
        orchestrator.test_tool_on_apk(
            client,
            tool_folder,
            api_key,
            apk_ref,
            args.tool_version,
            args.keep_artifacts,
            args.force_test,
        )
