from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class gator_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.FlowdroidLog4jError,
        errors.PythonError,
    ]
    TOOL_NAME = "gator"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        if len(list(path.glob("null-DEBUG-*.txt"))) == 0:
            return False
        with (path / "stdout").open("r", errors="replace") as file:
            for line in file:
                if "</GUIHierarchy>" in line:
                    return True
        return False
