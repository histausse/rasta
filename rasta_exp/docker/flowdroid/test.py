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

JAVA_PARAM = ""
WORKDIR = "/workspace/flowdroid"
JAR_FILE = "soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar"
CMD = f"java {JAVA_PARAM} -jar {JAR_FILE} -a {PATH_APK} -p /opt/android-sdk/platforms/ -s soot-infoflow-android/SourcesAndSinks.txt --mergedexfiles"

TOOL_NAME = "flowdroid"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
    "provided_build": "provided_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"

# TODO: add reg = re.compile(r"^\[main\] ERROR .*$", re.MULTILINE)
#       and strange backtrace without log4j prefixe
EXPECTED_ERROR_TYPES: list[Type[errors.LoggedError]] = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    errors.FlowdroidLog4jError,
]


success_re = re.compile(
    r"\[.*?\] INFO soot.jimple.infoflow.android.SetupApplication\$InPlaceInfoflow - Data flow solver took (\d*) seconds. Maximum memory consumption: (\d*) MB\n"
    r"\[.*?\] INFO soot.jimple.infoflow.android.SetupApplication - Found (\d*) leaks",
    re.MULTILINE,
)


def analyse_artifacts(path: Path) -> dict[str, Any]:
    """Analyse the artifacts of a test located at `path`."""
    report = utils.parse_report(path / "report")
    report["errors"] = list(
        map(
            lambda e: e.get_dict(),
            errors.get_errors(path / "stderr", EXPECTED_ERROR_TYPES),
        )
    )
    l1, l2 = "", ""
    # TODO: find a better way to do it
    with (path / "stderr").open("r", errors="replace") as file:
        for l in file:
            l1, l2 = l2, l
    last_lines = l1 + l2
    match = success_re.match(last_lines)
    tool_specific = {}
    if match is not None:
        tool_specific["time"] = int(match.group(1))
        tool_specific["mem"] = (
            int(match.group(2)) * 1024 * 1024
        )  # Memory unit is B, not MB
        tool_specific["nb_leaks_found"] = int(match.group(3))
    report["tool_specific"] = tool_specific

    if report["timeout"]:
        report["tool-status"] = "TIMEOUT"
    elif match is not None:
        report["tool-status"] = "FINISHED"
    else:
        report["tool-status"] = "FAILED"
    report["tool-name"] = TOOL_NAME
    report["date"] = str(datetime.datetime.now())
    report["apk"] = utils.sha256_sum(path / "app.apk").upper()
    return report


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
