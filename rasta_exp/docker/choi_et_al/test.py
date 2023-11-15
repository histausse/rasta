import datetime
import importlib.util
import logging
import re

from typing import Any, Type, Optional
from pathlib import Path
from more_itertools import peekable

#
#            ██╗    ██╗    ██╗    ██████╗
#            ██║    ██║    ██║    ██╔══██╗
#            ██║ █╗ ██║    ██║    ██████╔╝
#            ██║███╗██║    ██║    ██╔═══╝
#            ╚███╔███╔╝    ██║    ██║
#             ╚══╝╚══╝     ╚═╝    ╚═╝
#
# Looks like JADX is not good enought, waiting for the author response

if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent.parent))

import orchestrator

errors = orchestrator.error_collector
utils = orchestrator.utils


TIMEOUT = 900


GUEST_MNT = "/mnt"
PATH_APK = f"{GUEST_MNT}/app.apk"

WORKDIR = f"{GUEST_MNT}"
CMD = f"/workspace/run.sh"

TOOL_NAME = "choi_et_al"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"


class HaskellError(errors.LoggedError):
    error_re = re.compile(r"([a-zA-Z0-9])+: (.*)$")

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        origin: str,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.origin = origin
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self) -> str:
        return f"{self.origin}: {self.msg}"

    def get_dict(self) -> dict[str, Any]:
        return {
            "error_type": "haskell",
            "origin": self.origin,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["HaskellError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = HaskellError.error_re.match(line)
        if match is None:
            return None
        error = HaskellError(
            line_nb,
            line_nb,
            match.group(1),
            match.group(2),
        )
        next(logs)
        return error


EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    errors.JavaError,  # JADX
    errors.NoPrefixJavaError,
]
EXPECTED_ERROR_TYPES_STDERR: list[Type[errors.LoggedError]] = [
    errors.JavaError,  # JADX
    errors.NoPrefixJavaError,
    HaskellError,
]


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = list(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stderr", EXPECTED_ERROR_TYPES_STDERR),
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
    if report["exit-status"] != 0:
        return False
    # If jadx failed the tool failed
    if not (path / "app").exists():
        return False
    if len(list((path / "app").glob("**/*.java"))) == 0:
        return False
    l1 = False
    l2 = False
    with (path / "stdout").open("r", errors="replace") as file:
        for line in file:
            if l2 and line == "done.\n":
                return True
            else:
                l2 = False
            if l1 and "seconds in total" in line:
                l1 = False
                l2 = True
            else:
                l1 = False
            if line == "Points-to graph: \n":
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
