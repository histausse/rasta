import datetime
import importlib.util
import logging

from typing import Any, Type
from pathlib import Path

if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))

import orchestrator

errors = orchestrator.error_collector
utils = orchestrator.utils

TIMEOUT = 900

GUEST_MNT = "/mnt"
PATH_APK = f"{GUEST_MNT}/app.apk"

WORKDIR = "/workspace"
PARAM = "-Xmx4g -Xss4g"
CMD = f"./run.sh {PARAM}"

TOOL_NAME = "iccta"

# Version name -> folder name
TOOL_VERSIONS = {
    "provided_build": "provided_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "provided_build"

EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    errors.FlowdroidLog4jError,
]


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = list(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stderr", EXPECTED_ERROR_TYPES),
        )
    )
    report["errors"].extend(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stdout", EXPECTED_ERROR_TYPES),
        )
    )
    if report["timeout"]:
        report["tool-status"] = "TIMEOUT"
    elif check_success(path):
        report["tool-status"] = "FINISHED"
    else:
        report["tool-status"] = "FAILED"
    report["tool-name"] = TOOL_NAME
    report["date"] = str(datetime.datetime.now())
    report["apk"] = utils.sha256_sum(path / "app.apk").upper()
    return report


def check_success(path: Path) -> bool:
    """Check if the analysis finished without crashing."""
    l1 = False
    with (path / "stdout").open(errors="replace") as file:
        for line in file:
            if l1 and "Analysis has run for" in line:
                return True
            l1 = False
            if "Maximum memory consumption:" in line:
                l1 = True
    return False


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
