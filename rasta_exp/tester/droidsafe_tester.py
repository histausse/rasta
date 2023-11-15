from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type
from pathlib import Path


class droidsafe_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.DroidsafeLog4jError,
    ]
    TOOL_NAME = "droidsafe"

    def __init__(self):
        super().__init__()

    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        return (path / "droidsafe-gen" / "info-flow-results.txt").exists() and (
            path / "droidsafe-gen" / "template-spec.ssl"
        ).exists()
