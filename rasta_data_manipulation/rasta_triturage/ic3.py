import sqlite3
import csv
import sys
from pathlib import Path
from typing import Optional, Any
from matplotlib_venn import venn2  # type: ignore
from .utils import render

ERROR_CARACT = (
    "error_type",
    "error",
    "msg",
    "file",
    "function",
    "level",
    "origin",
    "raised_info",
    "called_info",
)
ERROR_MSG = " || '|' || ".join(map(lambda s: f"COALESCE({s}, '')", ERROR_CARACT))


def ic3_venn(db: Path, interactive: bool = True, image_path: Path | None = None):
    values = {
        ("FAILED", "NOT_FAILED"): 0,
        ("FAILED", "FAILED"): 0,
        ("NOT_FAILED", "FAILED"): 0,
    }
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for ic3_s, ic3_fork_s, n in cur.execute(
            "SELECT ex1.tool_status, ex2.tool_status, COUNT(*) "
            "FROM exec AS ex1 OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' "
            "GROUP BY ex1.tool_status, ex2.tool_status"
        ):
            if ic3_s == "FAILED" and ic3_fork_s == "FAILED":
                values[("FAILED", "FAILED")] += n
            elif ic3_s == "FAILED":
                values[("FAILED", "NOT_FAILED")] += n
            elif ic3_fork_s == "FAILED":
                values[("NOT_FAILED", "FAILED")] += n
    venn2(
        subsets=(
            values[("FAILED", "NOT_FAILED")],
            values[("NOT_FAILED", "FAILED")],
            values[("FAILED", "FAILED")],
        ),
        set_labels=("IC3 failed", "IC3 fork failed"),
    )
    render(
        "Number of application that IC3 \nand its fork failed to analyse",
        interactive,
        image_path,
    )


def ic3_errors(db: Path, file: Path | None = None):
    errors = []
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3_fork' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status = 'FAILED' AND ex2.tool_status != 'FAILED' "
            f"GROUP BY ex1.tool_status = 'FAILED', ex2.tool_status != 'FAILED', error.tool_name, error.error, {ERROR_MSG} "
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3_fork' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status != 'FAILED' AND ex2.tool_status = 'FAILED' "
            f"GROUP BY ex1.tool_status != 'FAILED', ex2.tool_status = 'FAILED', error.tool_name, error.error, {ERROR_MSG}"
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3_fork' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status = 'FAILED' AND ex2.tool_status = 'FAILED' "
            f"GROUP BY ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', error.tool_name, error.error, {ERROR_MSG} "
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status = 'FAILED' AND ex2.tool_status != 'FAILED' "
            f"GROUP BY ex1.tool_status = 'FAILED', ex2.tool_status != 'FAILED', error.tool_name, error.error, {ERROR_MSG} "
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status != 'FAILED' AND ex2.tool_status = 'FAILED' "
            f"GROUP BY ex1.tool_status != 'FAILED', ex2.tool_status = 'FAILED', error.tool_name, error.error, {ERROR_MSG} "
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
        for err in cur.execute(
            "SELECT ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', "
            "    error.tool_name, error.error, COUNT(DISTINCT error.sha256) AS cnt, "
            f"    {ERROR_MSG} "
            "FROM exec AS ex1 "
            "    OUTER LEFT JOIN exec AS ex2 ON ex1.sha256 = ex2.sha256 "
            "    INNER JOIN error ON ex1.sha256 = error.sha256 AND error.tool_name = 'ic3' "
            "WHERE ex1.tool_name = 'ic3' AND ex2.tool_name = 'ic3_fork' AND "
            "    ex1.tool_status = 'FAILED' AND ex2.tool_status = 'FAILED' "
            f"GROUP BY ex1.tool_status = 'FAILED', ex2.tool_status = 'FAILED', error.tool_name, error.error, {ERROR_MSG} "
            "ORDER BY cnt DESC "
            "LIMIT 10;"
        ):
            errors.append(err)
    if file is None:
        fp = sys.stdout
    else:
        fp = file.open("w")
    writer = csv.DictWriter(
        fp,
        fieldnames=[
            "ic3 failed",
            "ic3 fork failed",
            "tool",
            "error",
            "occurence",
            "msg",
        ],
    )
    writer.writeheader()
    for err in map(rewrite_msg, errors):
        writer.writerow(
            {
                k: v
                for k, v in zip(
                    [
                        "ic3 failed",
                        "ic3 fork failed",
                        "tool",
                        "error",
                        "msg",
                        "occurence",
                    ],
                    err,
                )
            }
        )
    if file is not None:
        fp.close()


def rewrite_msg(
    err: tuple[int, int, str, str, int, str]
) -> tuple[int, int, str, str, int, str]:
    ic3_failed, ic3_fork_failed, tool, error, occurence, msg = err
    (
        error_type,
        error,
        msg,
        file,
        function,
        level,
        origin,
        raised_info,
        called_info,
    ) = map(lambda s: "" if s == "" else s + " ", msg.split("|"))
    msg = f"{level}{error}{msg}{called_info}{called_info}{file}{function}{origin}"
    return (ic3_failed, ic3_fork_failed, tool, error, occurence, msg)
