import sqlite3
import sys
import csv

from pathlib import Path
from typing import Optional


def get_ressource(
    db: Path,
    folder: Optional[Path] = None,
):
    data_time = {}
    data_mem = {}
    tools = set()
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for tool, status, avg_time, var_time, avg_mem, var_mem in cur.execute(
            "SELECT tool_name, exec.tool_status, "
            "    AVG(time), AVG(time*time) - AVG(time)*AVG(time), "
            "    AVG(max_rss_mem), AVG(max_rss_mem*max_rss_mem) - AVG(max_rss_mem)*AVG(max_rss_mem) "
            "FROM exec "
            "GROUP BY tool_name, tool_status;"
        ):
            tools.add(tool)
            if var_time is None:
                var_time = 0
            if var_mem is None:
                var_mem = 0
            data_time[(tool, status)] = (avg_time, var_time ** (1 / 2))
            data_mem[(tool, status)] = (avg_mem, var_mem ** (1 / 2))
    fieldnames = list(tools)
    fieldnames.sort()
    fieldnames = ["", *fieldnames]
    if folder is None:
        fd_time = sys.stdout
        fd_mem = sys.stdout
    else:
        fd_time = (folder / "average_time.csv").open("w")
        fd_mem = (folder / "average_mem.csv").open("w")
    writer_time = csv.DictWriter(fd_time, fieldnames=fieldnames)
    writer_mem = csv.DictWriter(fd_mem, fieldnames=fieldnames)
    writer_time.writeheader()
    writer_mem.writeheader()
    for status in ("FINISHED", "FAILED", "TIMEOUT"):
        row_time = {"": status}
        row_mem = {"": status}
        for tool in tools:
            row_time[tool] = round(data_time.get((tool, status), (0, 0))[0], 2)
            row_mem[tool] = round(data_mem.get((tool, status), (0, 0))[0], 2)
        writer_time.writerow(row_time)
        writer_mem.writerow(row_mem)
        row_time = {"": "standard deviation"}
        row_mem = {"": "standard deviation"}
        for tool in tools:
            row_time[tool] = round(data_time.get((tool, status), (0, 0))[1], 2)
            row_mem[tool] = round(data_mem.get((tool, status), (0, 0))[1], 2)
        writer_time.writerow(row_time)
        writer_mem.writerow(row_mem)
    if folder is not None:
        fd_time.close()
        fd_mem.close()
