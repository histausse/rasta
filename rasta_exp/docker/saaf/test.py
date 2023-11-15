import datetime
import importlib.util
import logging
import xml.etree.ElementTree as xmltree
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

WORKDIR = "/workspace/saaf"

# JAVA_PARAM = "-Xms500M -Xmx500M"  # Default param from script: not enough memory
JAVA_PARAM = "-Xms500M -Xmx64G"
JAR_FILE = "/workspace/saaf/dist/SAAF.jar"
CMD = f"java {JAVA_PARAM} -Dfile.encoding=UTF-8 -jar {JAR_FILE} -hl -log {GUEST_MNT}/log.txt -nodb -rprt {GUEST_MNT}/rprt {PATH_APK}"

TOOL_NAME = "saaf"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"


class SaafLog4jError(errors.LoggedError):
    error_re = re.compile(
        r"\d\d .*? \d\d\d\d \d\d:\d\d:\d\d,\d*? \[.*?\] (ERROR|FATAL) (.*?) - (.*)$"
    )

    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        level: str,
        origin: str,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.level = level
        self.origin = origin
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self) -> str:
        return f"{self.level} {self.origin} {self.msg}"

    def get_dict(self) -> dict[str, Any]:
        return {
            "error_type": "Log4j",
            "level": self.level,
            "origin": self.origin,
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["SaafLog4jError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        match = SaafLog4jError.error_re.match(line)
        if match is None:
            return None
        error = SaafLog4jError(
            line_nb, line_nb, match.group(1), match.group(2), match.group(3)
        )
        next(logs)
        return error


EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    SaafLog4jError,
]


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = list(
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
    # uncritical = None
    critical = None
    with (path / "stdout").open("r", errors="replace") as stdout:
        for line in stdout:
            # if "#Analyses w/ uncritical exceptions:" in line:
            #    uncritical = int(
            #        line.removeprefix("#Analyses w/ uncritical exceptions:").strip()
            #    )
            if "#Critical Exceptions:" in line:
                critical = int(line.removeprefix("#Critical Exceptions:").strip())
    # if uncritical is None or critical is None:
    #    return False
    if critical is None:
        return False
    if critical != 0:
        return False
    rprts = list((path / "rprt").glob("*.xml"))
    if len(rprts) != 1:
        return False
    rprt = rprts[0]
    tree = xmltree.parse(rprt)
    msgs = tree.findall("./status/message")
    if len(msgs) != 1:
        return False
    msg = msgs[0]
    if msg.text != "FINISHED":
        return False
    return True


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
