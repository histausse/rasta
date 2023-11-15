from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path
from typing import Any, Type, Optional
from more_itertools import peekable
import xml.etree.ElementTree as xmltree


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

    def get_dict(self) -> dict:
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


class saaf_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        SaafLog4jError,
    ]
    TOOL_NAME = "saaf"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        # uncritical = None
        critical = None
        with (path / "stdout").open("r", errors="replace") as stdout:
            for line in stdout:
                # if "#Analyses w/ uncritical exceptions:" in line:
                #    uncritical = int(
                #        utils.removeprefix(line, "#Analyses w/ uncritical exceptions:").strip()
                #    )
                if "#Critical Exceptions:" in line:
                    critical = int(
                        utils.removeprefix(line, "#Critical Exceptions:").strip()
                    )
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
