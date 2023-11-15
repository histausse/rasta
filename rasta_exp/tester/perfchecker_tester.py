from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class perfchecker_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.FlowdroidLog4jError,
    ]
    TOOL_NAME = "perfchecker"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        START = "***********************analysis results**********************"
        END = "********************end of analysis results******************"
        started = False
        with (path / "stdout").open("r", errors="replace") as file:
            for line in file:
                if line.strip() == START:
                    started = True
                if started and line.strip() == END:
                    return True
        return False
