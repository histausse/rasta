from pathlib import Path
from typing import Any, Dict
import hashlib


def parse_report(report_file: Path) -> Dict[str, Any]:
    """Parse a report file."""
    report: dict[str, Any] = {}
    with report_file.open("r", errors="replace") as file:
        lines = file.readlines()
    for line in lines:
        k, v = map(lambda x: x.strip(), line.split(":"))
        if k in {"time", "kernel-cpu-time", "user-cpu-time"}:
            report[k] = float(v)
        else:
            report[k] = int(v)
    # TODO: normalize the mem values to Bytes (and not KB)
    #     Warning: page-size is already in B
    for k in ["max-rss-mem", "avg-rss-mem", "avg-total-mem"]:
        if k in report:
            report[k] *= 1024  # TODO: 1000 or 1024 (ie KiB or KB?)

    if "exit-status" in report:
        report["timeout"] = report["exit-status"] == 124
    return report


def sha256_sum(path: Path, chunk_size=4096) -> str:
    """Compute the sha256 of an apk."""
    hash = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash.update(chunk)
    return hash.hexdigest()


def removesuffix(string: str, suffix: str) -> str:
    """`str.removesuffix` for python < 3.9"""
    if string.endswith(suffix):
        return string[: -len(suffix)]
    return string


def removeprefix(string: str, prefix: str) -> str:
    """`str.removeprefix` for python < 3.9"""
    if string.startswith(prefix):
        return string[len(prefix):]
    else:
        return string
