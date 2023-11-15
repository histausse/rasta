from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
import re
from typing import Type
from pathlib import Path


class ic3_fork_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
      errors.JavaError,
      errors.NoPrefixJavaError,
    ]
    TOOL_NAME = "ic3_fork"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        return len(list((path / "ic3_out").iterdir())) >= 1
