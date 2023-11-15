from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class apparecium_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [errors.PythonError]
    TOOL_NAME = "apparecium"
    SOURCE_SINK_RE = re.compile(r"(\d+) sources, (\d+) sinks")

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        with (path / "stdout").open() as f:
            for line in f:
                m = apparecium_tester.SOURCE_SINK_RE.match(line)
                if m is not None and (int(m.group(1)) == 0 or int(m.group(2)) == 0):
                    return True
                if line.strip() in [
                    "potential data leakage: YES",
                    "potential data leakage: NO",
                ]:
                    return True
        return False
