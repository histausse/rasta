from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type
from pathlib import Path


class amandroid_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
    ]
    TOOL_NAME = "amandroid"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        return (
            path
            / "out"
            / utils.removesuffix(apk_filename, ".apk")
            / "result"
            / "AppData.txt"
        ).exists()
