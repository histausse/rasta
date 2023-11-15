from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type, Optional, Any
from pathlib import Path
import re
from more_itertools import peekable


# TODO: Why isn't that in error_collector with the other error types?
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
        raised_info: Optional[dict],
        called_info: Optional[dict],
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

    def get_dict(self) -> dict:
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
    def parse_error(logs: peekable) -> Optional["OcamlError"]:
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




class redexer_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [OcamlError, errors.RubyError]
    TOOL_NAME = 'redexer'
    EXPECTED_ERROR_TYPES_STDOUT: list = [
        errors.JavaError,  # For apktool
    ]  # TODO: add log4j format for apktool

    def __init__(self):
        super().__init__()


    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        new_apk = path / "new.apk"
        return new_apk.exists()

