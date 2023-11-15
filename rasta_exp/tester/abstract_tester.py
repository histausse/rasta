from abc import ABC, abstractmethod
from pathlib import Path
import utils
import datetime
import error_collector as errors


class abstract_tester(ABC):
    """
    Base class for too tester.
    Sub-classes MUST define TOOL_NAME and EXPECTED_ERROR_TYPES
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def analyse_artifacts(cls, path: Path, apk_filename: str):
        """Analyse the artifacts of a test located at `path`."""
        try:
            report = utils.parse_report(path / "report")
            report["errors"] = [
                e.get_dict()
                for e in errors.get_errors(path / "stderr", cls.EXPECTED_ERROR_TYPES)
            ]
            report["errors"].extend(
                [
                    e.get_dict()
                    for e in errors.get_errors(path / "stdout", cls.EXPECTED_ERROR_TYPES)
                ]
            )
            if report["timeout"]:
                report["tool-status"] = "TIMEOUT"
            elif cls.check_success(path, apk_filename):
                report["tool-status"] = "FINISHED"
            else:
                report["tool-status"] = "FAILED"
        except Exception as e:
            report = {}
            report["tool-status"] = "UNKNOWN"
            report["analyser-error"] = str(e)

        report["tool-name"] = cls.TOOL_NAME
        report["date"] = str(datetime.datetime.now())
        report["apk"] = apk_filename
        return report

    @classmethod
    @abstractmethod
    def check_success(cls, path: Path, apk_filename: str):
        pass
