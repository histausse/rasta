from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class flowdroid_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.FlowdroidLog4jError,
    ]
    TOOL_NAME = "flowdroid"
    RE_SUCCESS = re.compile(
        r"\[.*?\] INFO soot.jimple.infoflow.android.SetupApplication\$InPlaceInfoflow - Data flow solver took (\d*) seconds. Maximum memory consumption: (\d*) MB\n"
        r"\[.*?\] INFO soot.jimple.infoflow.android.SetupApplication - Found (\d*) leaks",
        re.MULTILINE,
    )

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        report = utils.parse_report(path / "report")
        l1, l2 = "", ""
        # TODO: find a better way to do it
        with (path / "stderr").open("r", errors="replace") as file:
            for l in file:
                l1, l2 = l2, l
        last_lines = l1 + l2
        match = flowdroid_tester.RE_SUCCESS.match(last_lines)
        return match is not None
