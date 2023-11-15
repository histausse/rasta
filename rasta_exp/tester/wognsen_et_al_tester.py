from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path
from typing import Optional
from more_itertools import peekable


class XsbError(errors.LoggedError):
    def __init__(
        self,
        first_line_nb: int,
        last_line_nb: int,
        msg: str,
        logfile_name: str = "",
    ):
        self.first_line_nb = first_line_nb
        self.last_line_nb = last_line_nb
        self.msg = msg
        self.logfile_name = logfile_name

    def __str__(self):
        return f"++Error{self.msg}"

    def get_dict(self) -> dict:
        return {
            "error_type": "Xsb",
            "msg": self.msg,
            "first_line": self.first_line_nb,
            "last_line": self.last_line_nb,
            "logfile_name": self.logfile_name,
        }

    @staticmethod
    def parse_error(logs: peekable) -> Optional["XsbError"]:
        line_nb, line = logs.peek((None, None))
        if line is None or line_nb is None:
            return None
        if not line.startswith("++Error"):
            return None
        error = XsbError(line_nb, line_nb, line.strip())
        next(logs)
        return error


class wognsen_et_al_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.PythonError,
        XsbError,
    ]
    TOOL_NAME = "wognsen_et_al"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        # The tool is supposed to print the graph to stdout, if stdout
        # is empty, it means the tool failed.
        return (path / "stdout").stat().st_size > 1
