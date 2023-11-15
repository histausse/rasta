from .abstract_tester import abstract_tester
import utils
import error_collector as errors
import datetime
from typing import Type
from pathlib import Path

class didfail_tester(abstract_tester):
    EXPECTED_ERROR_TYPES: list = [errors.PythonError]
    TOOL_NAME = 'didfail'
    EXPECTED_ERROR_TYPES_FLOWDROID: list = [
    errors.JavaError,
    errors.NoPrefixJavaError,
    errors.FlowdroidLog4jError,
    ]
    EXPECTED_ERROR_TYPES_XFORM: list = [
        errors.JavaError,
        errors.NoPrefixJavaError,
        errors.FlowdroidLog4jError,
    ]

    EXPECTED_ERROR_TYPES_DARE: list = []


    def __init__(self):
        super().__init__()


    @classmethod
    def analyse_artifacts(cls, path: Path, apk_filename: str):
        """Analyse the artifacts of a test located at `path`."""
        apk_basename = apk_filename.rstrip('.apk')
        report = utils.parse_report(path / "report")
        report["errors"] = []
        flowdroid_log = path / "out" / "log" / (apk_basename+".flowdroid.log")
        dare_log = path / "out" / "log" / (apk_basename+".dare.log")
        xform_log = path / "out" / "log" / (apk_basename+".xform.log")
        report["errors"].extend(
            [e.get_dict() for e in errors.get_errors(path / "stdout", cls.EXPECTED_ERROR_TYPES)]
        )
        if flowdroid_log.exists():
            report["errors"].extend(
                [e.get_dict() for e in errors.get_errors(flowdroid_log, cls.EXPECTED_ERROR_TYPES_FLOWDROID)]
            )
        if dare_log.exists():
            report["errors"].extend(
                [e.get_dict() for e in errors.get_errors(dare_log, cls.EXPECTED_ERROR_TYPES_DARE)]
            )
        if xform_log.exists():
            report["errors"].extend(
                [e.get_dict() for e in errors.get_errors(xform_log, cls.EXPECTED_ERROR_TYPES_XFORM)]
            )

        if report["timeout"]:
            report["tool-status"] = "TIMEOUT"
        elif cls.check_success(path, apk_filename) and (report["exit-status"] == 0):
            report["tool-status"] = "FINISHED"
        else:
            report["tool-status"] = "FAILED"
        report["tool-name"] = cls.TOOL_NAME
        report["date"] = str(datetime.datetime.now())
        report["apk"] = apk_filename
        return report




    @classmethod
    def check_success(cls, path: Path, apk_filename: str):
        """Check if the analysis finished without crashing."""
        with (path / "stdout").open("r", errors="replace") as file:
            for line in file:
                if line == "Failure!\n":
                    return False
        flowfile = path / "out" / "flows.out"
        if not flowfile.exists():
            return False
        return flowfile.stat().st_size > 1
