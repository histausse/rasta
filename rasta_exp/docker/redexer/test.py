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

WORKDIR = "/workspace/redexer"
SCRIP = "/workspace/redexer/scripts/cmd.rb"
CMD = f"ruby {SCRIP} {PATH_APK} --cmd logging --outputdir {GUEST_MNT}/ --to {GUEST_MNT}/new.apk"

TOOL_NAME = "redexer"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"


class OcamlError(errors.LoggedError):
    error_re = re.compile(r"(Exception|Fatal error): (.*)")
    raised_at_re = re.compile(
        r"Raised at (.*?) in file \"(.*?)\", line (\d*?), characters .*"
    )
    called_from_re = re.compile(
        r"Called from (.*?) in file \"(.*?)\", line (\d*?), characters .*"
    )

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        level: str,
        msg: str,
        raised_info: Optional[dict[str, Any]],
        called_info: Optional[dict[str, Any]],
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.level = level
        self.msg = msg
        self.raised_info = raised_info
        self.called_info = called_info
        self.logfile_name = logfile_name

    def __str__(self):
        l1 = f"{self.level}: {self.msg}"
        if self.raised_info is not None:
            l2 = f"\nRaised at {self.raised_info['function']} in file \"{self.raised_info['file']}\", line {self.raised_info['line']}"
        else:
            l2 = ""
        if self.called_info is not None:
            l2 = f"\nCalled from {self.called_info['function']} in file \"{self.called_info['file']}\", line {self.called_info['line']}"
        else:
            l2 = ""

        return f"{self.level}: {self.msg}"

    def get_dict(self) -> dict[str, Any]:
        return {
            "error_type": "Ocaml",
            "level": self.level,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "raised_info": self.raised_info,
            "called_info": self.called_info,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: "peekable[tuple[int, str]]") -> Optional["OcamlError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = OcamlError.error_re.match(line)
        if match is None:
            return None
        error = OcamlError(line_nb, line_nb, match.group(1), match.group(2), None, None)
        next(logs)
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return error
        match = OcamlError.raised_at_re.match(line)
        if match is None:
            return error
        error.raised_info = {
            "function": match.group(1),
            "file": match.group(2),
            "line": match.group(3),
        }
        next(logs)
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return error
        match = OcamlError.called_from_re.match(line)
        if match is None:
            return error
        error.called_info = {
            "function": match.group(1),
            "file": match.group(2),
            "line": match.group(3),
        }

        return error


EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    OcamlError,
    errors.RubyError,
]

EXPECTED_ERROR_TYPES_STDOUT: list[Type[errors.LoggedError]] = [
    errors.JavaError,  # For apktool
]  # TODO: add log4j format for apktool


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
            errors.get_errors(path / "stdout", EXPECTED_ERROR_TYPES_STDOUT),
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
    new_apk = path / "new.apk"
    return new_apk.exists()


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
