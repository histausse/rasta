from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type
from pathlib import Path

class blueseal_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [errors.JavaError, errors.NoPrefixJavaError]
    TOOL_NAME = 'blueseal'


    def __init__(self):
        super().__init__()


    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        l1 = False
        with (path / "stdout").open("r", errors="replace") as stdout:
            for line in stdout:
                if l1 and "Soot has run for " in line:
                    return True
                l1 = False
                if "Soot finished on " in line:
                    l1 = True
        return False


