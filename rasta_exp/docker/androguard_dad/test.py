import datetime
import importlib.util
import logging

from typing import Any, Type
from pathlib import Path

if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))

#import orchestrator

errors = orchestrator.error_collector
utils = orchestrator.utils

TIMEOUT = 900

GUEST_MNT = "/mnt"
PATH_APK = f"{GUEST_MNT}/app.apk"

WORKDIR = "/"
CMD = f"androguard decompile -o {GUEST_MNT}/out {PATH_APK}"

TOOL_NAME = "androguard"

# Version name -> folder name
TOOL_VERSIONS = {
    "v3.3.5": "v3_3_5",
    # "latest": "latest_2022", # the current master is not stable
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "v3.3.5"

EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [errors.PythonError]


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = list(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stderr", EXPECTED_ERROR_TYPES),
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
    stdout = path / "stdout"
    with stdout.open("r", errors="replace") as f:
        for line in f:
            if (
                "ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS."
                in line
            ):
                return True
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
