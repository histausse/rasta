from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class mallodroid_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.PythonError
    ]
    TOOL_NAME = "mallodroid"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        stdout = path / "stdout"
        with stdout.open("r", errors="replace") as f:
           for line in f:
               if "ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS." in line:
                   return True
        return False
