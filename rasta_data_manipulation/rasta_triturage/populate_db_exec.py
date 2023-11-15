import sqlite3
import json
import datetime
from pathlib import Path

from .query_error import estimate_cause


def create_tables(db: Path):
    """Create the db/tables if they do not exist."""
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(
            (
                "CREATE TABLE IF NOT EXISTS exec ("
                "    sha256, id, rev, time, kernel_cpu_time, user_cpu_time, "
                "    max_rss_mem, avg_rss_mem, avg_total_mem, page_size, "
                "    nb_major_page_fault, nb_minor_page_fault, nb_fs_input, "
                "    nb_fs_output, nb_socket_msg_received, nb_socket_msg_sent, "
                "    nb_signal_delivered, exit_status, timeout, "
                "    tool_status, tool_name, date date"
                ");"
            )
        )
        cur.execute(
            (
                "CREATE TABLE IF NOT EXISTS error ("
                "    tool_name, sha256, error_type, error, msg, "
                "    first_line, last_line, logfile_name, file, "
                "    line, function, level, origin, raised_info, "
                "    called_info, cause"
                ");"
            )
        )
        con.commit()


def insert_errors(cur, tool, sha256, errors):
    for error in errors:
        error["tool_name"] = tool
        error["sha256"] = sha256
        error.setdefault("error_type", None)
        error.setdefault("error", None)
        error.setdefault("msg", None)
        error.setdefault("first_line", None)
        error.setdefault("last_line", None)
        error.setdefault("logfile_name", None)
        error.setdefault("file", None)
        error.setdefault("line", None)
        error.setdefault("function", None)
        error.setdefault("level", None)
        error.setdefault("origin", None)
        error.setdefault("raised_info", None)
        if error["raised_info"] is not None:
            error["raised_info"] = 'Raised at {} in file "{}", line {}'.format(
                error["raised_info"]["function"],
                error["raised_info"]["file"],
                error["raised_info"]["line"],
            )
        error.setdefault("called_info", None)
        if error["called_info"] is not None:
            error["called_info"] = 'Called from {} in file "{}", line {}'.format(
                error["called_info"]["function"],
                error["called_info"]["file"],
                error["called_info"]["line"],
            )
        # The stack strace can be quite big without being very usefull in
        # queries
        error.pop("stack", None)
    cur.executemany(
        (
            "INSERT INTO error VALUES("
            "    :tool_name, :sha256, :error_type, :error, :msg, "
            "    :first_line, :last_line, :logfile_name, :file, "
            "    :line, :function, :level, :origin, :raised_info, "
            "    :called_info, ''"
            ");"
        ),
        errors,
    )


def fix_error(db: Path, report_with_correct_error: Path):
    """Infortunatly they was some errors in parsing the errors during the experiment,
    some another run was made for some pair of tool-apk to get the actual error.
    This pass was made in a different environnment (!= memory and space constraint),
    so we only replace the errors (after manual inspection, they don't seam related
    to the environnment), and keep the other values from the original experiment.
    """
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for path in report_with_correct_error.iterdir():
            with path.open() as f:
                exec_log = json.load(f)
            sha256 = exec_log["apk"].removesuffix(".apk")
            if (
                len(
                    cur.execute(
                        "SELECT * FROM exec WHERE tool_name = ? AND sha256 = ?",
                        (exec_log["tool-name"], sha256),
                    ).fetchall()
                )
                == 1
            ):
                cur.execute(
                    "DELETE FROM error WHERE tool_name = ? AND sha256 = ?",
                    (exec_log["tool-name"], sha256),
                )
                errors = exec_log.pop("errors", [])
                insert_errors(cur, exec_log["tool-name"], sha256, errors)
        con.commit()


def populate_execution_report(db: Path, report_folder: Path):
    """Add to database the report stored in the report_folder."""
    create_tables(db)
    i = 0
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for path in report_folder.iterdir():
            with path.open() as f:
                exec_log = json.load(f)
            exec_log["sha256"] = exec_log["apk"].removesuffix(".apk")
            exec_log["id"] = exec_log.get("_id", None)
            exec_log["rev"] = exec_log.get("_rev", None)
            errors = exec_log.pop("errors", [])

            exec_log["date"] = (
                datetime.datetime.fromisoformat(exec_log["date"])
                if exec_log.get("date", None)
                else None
            )
            del exec_log["apk"]
            if "_id" in exec_log:
                del exec_log["_id"]
            if "_rev" in exec_log:
                del exec_log["_rev"]
            new_exec_log = {}
            for key in exec_log:
                new_key = key.replace("-", "_")
                new_exec_log[new_key] = exec_log[key]
            for val in [
                "sha256",
                "id",
                "rev",
                "time",
                "kernel_cpu_time",
                "user_cpu_time",
                "max_rss_mem",
                "avg_rss_mem",
                "avg_total_mem",
                "page_size",
                "nb_major_page_fault",
                "nb_minor_page_fault",
                "nb_fs_input",
                "nb_fs_output",
                "nb_socket_msg_received",
                "nb_socket_msg_sent",
                "nb_signal_delivered",
                "exit_status",
                "timeout",
                "tool_status",
                "tool_name",
                "date",
            ]:
                if val not in new_exec_log:
                    new_exec_log[val] = None
            cur.execute(
                (
                    "INSERT INTO exec VALUES("
                    "    :sha256, :id, :rev, :time, :kernel_cpu_time, :user_cpu_time, "
                    "    :max_rss_mem, :avg_rss_mem, :avg_total_mem, :page_size, "
                    "    :nb_major_page_fault, :nb_minor_page_fault, :nb_fs_input, "
                    "    :nb_fs_output, :nb_socket_msg_received, :nb_socket_msg_sent, "
                    "    :nb_signal_delivered, :exit_status, :timeout, "
                    "    :tool_status, :tool_name, :date"
                    ");"
                ),
                new_exec_log,
            )
            insert_errors(cur, exec_log["tool-name"], exec_log["sha256"], errors)
            i += 1
            if i == 10_000:
                # Not sure how much ram would be needed to commit in one go
                con.commit()
        con.commit()
