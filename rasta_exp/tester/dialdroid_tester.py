from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class dialdroid_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.FlowdroidLog4jError,
    ]
    TOOL_NAME = "dialdroid"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        l1 = False
        l2 = False
        with (path / "stdout").open(errors="replace") as file:
            for line in file:
                if (
                    l2
                    and line.strip()
                    == f"Done:{utils.removesuffix(apk_filename.lower(), '.apk')}"
                ):
                    return True
                l2 = False
                if l1 and "Analysis has run for" in line:
                    l2 = True
                l1 = False
                if "Maximum memory consumption:" in line:
                    l1 = True

        return False
