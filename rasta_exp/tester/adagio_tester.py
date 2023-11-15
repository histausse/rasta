from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type
from pathlib import Path

class adagio_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [errors.PythonError]
    TOOL_NAME = 'adagio'


    def __init__(self):
        super().__init__()


    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        apks = list(path.glob("*.apk"))
        if len(apks) != 1:
            raise RuntimeError(
                # FIXME: do not raise in check_success. Return False instead
                f"Expected to found exactly 1 apk in the root of  artifact folder, found {apks}"
            )
        apk = apks[0]
        path_result = path / utils.sha256_sum(apk).lower()
        return path_result.exists()

