import datetime
import importlib.util
import logging

from typing import Any
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

JAVA_PARAM = "-XX:MaxPermSize=512m -Xms512m  -Xmx1024M -Xss1024m"
WORKDIR = "/workspace/pushdownoo/pdafordalvik"
JAR_FILE = "/workspace/pushdownoo/pdafordalvik/artifacts/PushdownOO_Exflow.jar"
# CMD = f"java {JAVA_PARAM} -jar {JAR_FILE} org.ucombinator.dalvik.cfa.cesk.RunAnalysis --k 1 --gc --lra --aco --godel --dump-graph {PATH_APK}"  # --dump-graph takes so much time!
CMD = f"java {JAVA_PARAM} -jar {JAR_FILE} org.ucombinator.dalvik.cfa.cesk.RunAnalysis --k 1 --gc --lra --aco --godel {PATH_APK}"

TOOL_NAME = "anadroid"

# Version name -> folder name
TOOL_VERSIONS = {
    "home_build": "home_build",
    "provided_build": "provided_build",
}
# Name of the default version (default folder = TOOL_VERSIONS[DEFAULT_TOOL_VERSION])
DEFAULT_TOOL_VERSION = "home_build"

EXPECTED_ERROR_TYPES = [errors.JavaError, errors.PythonError]


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
        # Check if the version of the tool used is the one with the add println
        modified_version = (
            "ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: START OF ANALYSIS."
            in f.readline()
        )
    with stdout.open("r", errors="replace") as f:
        for line in f:
            if modified_version and (
                "ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS."
                in line
            ):
                return True
            # If we use the orginal tool and the tool worked, this line should appear
            # WARNING: the path to the graph depend on the name and location of the app, the one
            #     use hear is the one for /mnt/app.apk
            if (
                not modified_version
                and "--dump-graph" in CMD
                and "Dyck State Graph dumped into /mnt/app/graphs/graph-1-pdcfa-gc-lra.dot"
                in line
            ):
                return True
            if (
                not modified_version
                and "--dump-graph" not in CMD
                and "Dyck State Graph dumped into /mnt/app/graphs/graph-1-pdcfa-gc-lra.dot"
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
