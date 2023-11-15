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


class DroidsafeLog4jError(errors.LoggedError):
    error_re = re.compile(r"(ERROR|FATAL): (.*)")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        level: str,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.level = level
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self) -> str:
        return f"{self.level}: {self.msg}"

    def get_dict(self) -> dict[str, Any]:
        return {
            "error_type": "Log4jSimpleMsg",
            "level": self.level,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["DroidsafeLog4jError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = DroidsafeLog4jError.error_re.match(line)
        if match is None:
            return None
        error = DroidsafeLog4jError(line_nb, line_nb, match.group(1), match.group(2))
        next(logs)
        return error


TIMEOUT = 900  # Doc says up to 2 hours


GUEST_MNT = "/mnt"
PATH_APK = f"{GUEST_MNT}/app.apk"

WORKDIR = "/mnt"
CMD = "make -f /workspace/Makefile specdump-apk"

TOOL_NAME = "droidsafe"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"

EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    DroidsafeLog4jError,
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
    return (path / "droidsafe-gen" / "info-flow-results.txt").exists() and (
        path / "droidsafe-gen" / "template-spec.ssl"
    ).exists()


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
