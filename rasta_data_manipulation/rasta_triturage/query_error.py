import sqlite3
import sys
import csv
import matplotlib.pyplot as plt  # type: ignore
from .utils import get_list_tools, radar_chart, render
from pathlib import Path
from typing import Optional, Any

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

# Query that remove identical error that occure multiple times on the same execution
DISTINCT_ERRORS = (
    "("
    f"    SELECT DISTINCT tool_name, sha256, {', '.join(ERROR_CARACT)}"
    "    FROM error"
    ") AS distinct_error"
)
DISTINCT_ERROR_CLASS = (
    "("
    f"    SELECT DISTINCT tool_name, sha256, error, error_type"
    "    FROM error"
    ") AS distinct_error"
)
DISTINCT_CAUSES = (
    "("
    "    SELECT DISTINCT tool_name, sha256, cause"
    "    FROM error"
    ") AS distinct_cause"
)


def estimate_cause(db: Path):
    """Estimate the cause of an error to easier grouping."""
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute("UPDATE error SET cause = '';")
        con.commit()
        # brut.androlib is package defined in apktool
        # 'Expected: 0x001c0001, got: 0x00000000' errors are always
        #  part of an apktool stacktrace:
        #    SELECT COUNT(*) FROM error e1
        #    WHERE e1.tool_name = '${tool}' AND
        #      e1.msg = 'Expected: 0x001c0001, got: 0x00000000' AND
        #      e1.sha256 NOT IN (
        #        SELECT e2.sha256 FROM error e2
        #        WHERE e2.tool_name = '${tool}' AND
        #          e2.msg LIKE '%Could not decode arsc file%'
        #      )
        #    is always 0"
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'apktool' "
                "WHERE error = 'brut.androlib.AndrolibException' OR "
                "    error LIKE 'brut.androlib.err.%' OR "
                "    msg = 'Expected: 0x001c0001, got: 0x00000000' OR "
                "    msg LIKE '%brut.androlib.AndrolibException: Could not decode arsc file%' OR "
                "    msg LIKE 'bad magic value: %' OR "
                "    error = 'brut.androlib.err.UndefinedResObject';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'memory' "
                "WHERE error = 'java.lang.StackOverflowError' OR "
                "    error = 'java.lang.OutOfMemoryError' OR "
                "    msg LIKE '%java.lang.OutOfMemoryError%' OR "
                "    msg LIKE '%java.lang.StackOverflowError%' OR "
                "    msg = 'Stack overflow';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'soot' "
                "WHERE msg LIKE ? OR "
                "    msg LIKE '%No call graph present in Scene. Maybe you want Whole Program mode (-w)%' OR "
                "    msg LIKE '%There were exceptions during IFDS analysis. Exiting.%' OR "  # More hero than soot?
                "    msg = 'Could not find method' OR "
                "    msg = 'No sources found, aborting analysis' OR "
                "    msg = 'No sources or sinks found, aborting analysis' OR "
                "    msg = 'Only phantom classes loaded, skipping analysis...';"
            ),
            (
                "%RefType java.lang.Object not loaded. If you tried to get the RefType of a library class, did you call loadNecessaryClasses()? Otherwise please check Soot's classpath.%",
            ),
        )

        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'index error' "
                "WHERE error = 'IndexError' OR "
                "    msg = 'java.lang.ArrayIndexOutOfBoundsException' OR "
                "    (error_type = 'Python' AND error = 'KeyError') OR "
                "    error = 'java.lang.IndexOutOfBoundsException' OR "
                "    error = 'java.lang.ArrayIndexOutOfBoundsException' OR "
                "    msg LIKE 'java.lang.ArrayIndexOutOfBoundsException:%';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'arithmetique' "
                "WHERE error = 'java.lang.ArithmeticException';"
            )
        )
        cur.execute("UPDATE error SET cause = 'jasmin' WHERE error = 'jas.jasError';")
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'storage' "
                "WHERE msg = 'No space left on device' OR "
                "    msg LIKE 'Error copying file: %' OR "
                "    msg = 'java.io.IOException: No space left on device';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'redexe pattern maching failed' "
                "WHERE msg  = 'File \"src/ext/logging.ml\", line 712, characters 12-17: Pattern matching failed';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'null pointer' "
                "WHERE error = 'java.lang.NullPointerException' OR "
                "    msg LIKE ? OR "
                "    msg LIKE 'undefined method % for nil:NilClass (NoMethodError)';"
            ),
            ("'NoneType' object has no attribute %",),
        )
        # Soot ?
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'unknown error in thread' "
                "WHERE msg = 'Worker thread execution failed: null';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'timeout' "
                "WHERE error = 'java.util.concurrent.TimeoutException';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'file name too long' "
                "WHERE msg = 'File name too long';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'encoding' "
                "WHERE error = 'UnicodeEncodeError';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'smali' "
                "WHERE error LIKE 'org.jf.dexlib2.%' OR error LIKE 'org.jf.util.%';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'redexer dex parser' "
                "WHERE msg LIKE 'Dex.Wrong_dex(\"%\")';"
            )
        )
        cur.execute(
            (
                "UPDATE error "
                "SET cause = 'bytecode not found' "
                "WHERE msg LIKE 'No method source set for method %' OR "
                "    msg LIKE '% is an system library method.' OR "
                "    msg LIKE '% is an unknown method.';"
            )
        )
        con.commit()
        # Default
        #        default = " || '|' || ".join(map(lambda s: f"COALESCE({s}, '')", ERROR_CARACT))
        #        cur.execute(f"UPDATE error SET cause = {default} WHERE cause = '';")
        cur.execute("UPDATE error SET cause = 'other' WHERE cause = '';")
        con.commit()


def radar_cause_estimation(
    db: Path,
    tools: list[str] | None,
    interactive: bool,
    folder: Path | None,
):
    # estimate_cause(db)
    if tools is None:
        tools = get_list_tools(db)

    with sqlite3.connect(db, timeout=60) as con:
        cur = con.cursor()
        causes = [
            v for v, in cur.execute("SELECT DISTINCT cause FROM error;").fetchall()
        ]
        for tool in tools:
            print(f"tool: {tool}")
            for cause, count in cur.execute(
                (
                    "SELECT cause, COUNT(*) AS cnt "
                    "FROM error "
                    "WHERE tool_name = ? "
                    "GROUP BY cause "
                    "ORDER BY cnt DESC LIMIT 10;"
                ),
                (tool,),
            ):
                print(f"{count: 6}: {cause}")
            print()

    values = []
    labels = tools
    for tool in tools:
        vals = [0 for _ in causes]
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            for cause, cnt in cur.execute(
                (
                    "SELECT distinct_cause.cause, COUNT(*) AS cnt "
                    f"FROM {DISTINCT_CAUSES} "
                    "WHERE distinct_cause.cause != '' AND distinct_cause.tool_name = ? "
                    "GROUP BY distinct_cause.cause;"
                ),
                (tool,),
            ):
                print(f"{tool=}, {cause=}, {cnt=}")
                if cause in causes:
                    vals[causes.index(cause)] = cnt
        print(f"{tool=}, {vals=}")
        radar_chart(
            causes, [vals], [tool], f"Causes of error for {tool}", interactive, folder
        )
        values.append(vals)
    radar_chart(causes, values, labels, "Causes of error", interactive, folder)


def get_common_errors(
    db: Path,
    tool: Optional[str] = None,
    status: Optional[str] = None,
    use_androguard: Optional[bool] = None,
    use_java: Optional[bool] = None,
    use_prolog: Optional[bool] = None,
    use_ruby: Optional[bool] = None,
    use_soot: Optional[bool] = None,
    use_apktool: Optional[bool] = None,
    use_ocaml: Optional[bool] = None,
    use_python: Optional[bool] = None,
    use_scala: Optional[bool] = None,
    folder: Optional[Path] = None,
    limit: int = 10,
):
    """Get the most common errors"""
    args: dict[str, Any] = {"limit": limit}
    clauses = []
    if tool is not None:
        clauses.append("(distinct_error.tool_name = :tool)")
        args["tool"] = tool
    if status is not None:
        clauses.append("(exec.tool_status = :tool_status)")
        args["tool_status"] = status

    if use_java is not None:
        clauses.append("(tool.use_java = :use_java)")
        args["use_java"] = use_java
    if use_prolog is not None:
        clauses.append("(tool.use_prolog = :use_prolog)")
        args["use_prolog"] = use_prolog
    if use_ruby is not None:
        clauses.append("(tool.use_ruby = :use_ruby)")
        args["use_ruby"] = use_ruby
    if use_soot is not None:
        clauses.append("(tool.use_soot = :use_soot)")
        args["use_soot"] = use_soot
    if use_apktool is not None:
        clauses.append("(tool.use_apktool = :use_apktool)")
        args["use_apktool"] = use_apktool
    if use_ocaml is not None:
        clauses.append("(tool.use_ocaml = :use_ocaml)")
        args["use_ocaml"] = use_ocaml
    if use_python is not None:
        clauses.append("(tool.use_python = :use_python)")
        args["use_python"] = use_python
    if use_scala is not None:
        clauses.append("(tool.use_scala = :use_scala)")
        args["use_scala"] = use_scala
    where_clause = ""
    if clauses:
        where_clause = f"WHERE {' AND '.join(clauses)}"

    # print(
    #     (
    #         f"SELECT COUNT(*) AS cnt, {', '.join(ERROR_CARACT)} \n"
    #         f"FROM {DISTINCT_ERRORS} \n"
    #         "INNER JOIN tool ON distinct_error.tool_name = tool.tool_name \n"
    #         "INNER JOIN exec ON \n"
    #         "    distinct_error.tool_name = exec.tool_name AND \n"
    #         "    distinct_error.sha256 = exec.sha256 \n"
    #         f"{where_clause}\n"
    #         f"GROUP BY {', '.join(ERROR_CARACT)} \n"
    #         "ORDER BY cnt DESC LIMIT :limit;\n"
    #     )
    # )
    # print(args)

    if folder is None:
        out = sys.stdout
    else:
        # Generate filename
        features = [
            use_androguard,
            use_java,
            use_prolog,
            use_ruby,
            use_soot,
            use_apktool,
            use_ocaml,
            use_python,
            use_scala,
        ]

        if tool is None:
            tool_str = ""
        else:
            tool_str = f"_for_{tool}"
        if status is None:
            status_str = ""
        else:
            status_str = f"_when_{status}"
        if all(map(lambda x: x is None, features)):
            features_str = ""
        else:
            features_str = "_using"
            if use_androguard:
                features_str += "_androguard"
            if use_java:
                features_str += "_java"
            if use_prolog:
                features_str += "_prolog"
            if use_ruby:
                features_str += "_ruby"
            if use_soot:
                features_str += "_soot"
            if use_apktool:
                features_str += "_apktool"
            if use_ocaml:
                features_str += "_ocaml"
            if use_python:
                features_str += "_python"
            if use_scala:
                features_str += "_scala"

        name = f"{limit}_most_common_errors{tool_str}{status_str}{features_str}.csv"
        # make sure the folder exist
        folder.mkdir(parents=True, exist_ok=True)
        out = (folder / name).open("w")

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        writer = csv.DictWriter(out, fieldnames=["error", "msg", "count"])
        writer.writeheader()
        for row in cur.execute(
            (
                f"SELECT COUNT(*) AS cnt, {', '.join(ERROR_CARACT)} "
                f"FROM {DISTINCT_ERRORS} "
                "INNER JOIN tool ON distinct_error.tool_name = tool.tool_name "
                "INNER JOIN exec ON "
                "    distinct_error.tool_name = exec.tool_name AND "
                "    distinct_error.sha256 = exec.sha256 "
                f"{where_clause}"
                f"GROUP BY {', '.join(ERROR_CARACT)} "
                "ORDER BY cnt DESC LIMIT :limit;"
            ),
            args,
        ):
            row_d = {k: v for (k, v) in zip(("cnt", *ERROR_CARACT), row)}
            writer.writerow(reduce_error_row(row_d))
    if folder is not None:
        out.close()


def reduce_error_row(row: dict[str, Any]) -> dict[str, Any]:
    """Reduce an error from an sqlite row to a simpler row for svg."""
    new_row = {}
    new_row["error"] = row["error"]
    msg = row["msg"]
    error = row["error"]
    if error:
        error += " "
    else:
        error = ""
    if msg:
        msg += " "
    else:
        msg = ""
    file = row["file"]
    if file:
        file += " "
    else:
        file = ""
    function = row["function"]
    if function:
        function += " "
    else:
        function = ""
    level = row["level"]
    if level:
        level += " "
    else:
        level = ""
    origin = row["origin"]
    if origin:
        origin += " "
    else:
        origin = ""
    raised_info = row["raised_info"]
    if raised_info:
        raised_info += " "
    else:
        raised_info = ""
    called_info = row["called_info"]
    if called_info:
        called_info += " "
    else:
        called_info = ""
    new_row[
        "msg"
    ] = f"{level}{error}{msg}{called_info}{called_info}{file}{function}{origin}"

    new_row["count"] = row["cnt"]
    return new_row


def get_common_error_classes(
    db: Path,
    tool: Optional[str] = None,
    status: Optional[str] = None,
    use_androguard: Optional[bool] = None,
    use_java: Optional[bool] = None,
    use_prolog: Optional[bool] = None,
    use_ruby: Optional[bool] = None,
    use_soot: Optional[bool] = None,
    use_apktool: Optional[bool] = None,
    use_ocaml: Optional[bool] = None,
    use_python: Optional[bool] = None,
    use_scala: Optional[bool] = None,
    folder: Optional[Path] = None,
    limit: int = 10,
):
    """Get the most common errors classes"""
    args: dict[str, Any] = {"limit": limit}
    clauses = []
    if tool is not None:
        clauses.append("(distinct_error.tool_name = :tool)")
        args["tool"] = tool
    if status is not None:
        clauses.append("(exec.tool_status = :tool_status)")
        args["tool_status"] = status

    if use_java is not None:
        clauses.append("(tool.use_java = :use_java)")
        args["use_java"] = use_java
    if use_prolog is not None:
        clauses.append("(tool.use_prolog = :use_prolog)")
        args["use_prolog"] = use_prolog
    if use_ruby is not None:
        clauses.append("(tool.use_ruby = :use_ruby)")
        args["use_ruby"] = use_ruby
    if use_soot is not None:
        clauses.append("(tool.use_soot = :use_soot)")
        args["use_soot"] = use_soot
    if use_apktool is not None:
        clauses.append("(tool.use_apktool = :use_apktool)")
        args["use_apktool"] = use_apktool
    if use_ocaml is not None:
        clauses.append("(tool.use_ocaml = :use_ocaml)")
        args["use_ocaml"] = use_ocaml
    if use_python is not None:
        clauses.append("(tool.use_python = :use_python)")
        args["use_python"] = use_python
    if use_scala is not None:
        clauses.append("(tool.use_scala = :use_scala)")
        args["use_scala"] = use_scala
    where_clause = ""
    if clauses:
        where_clause = f"WHERE {' AND '.join(clauses)}"

    if folder is None:
        out = sys.stdout
    else:
        # Generate filename
        features = [
            use_androguard,
            use_java,
            use_prolog,
            use_ruby,
            use_soot,
            use_apktool,
            use_ocaml,
            use_python,
            use_scala,
        ]

        if tool is None:
            tool_str = ""
        else:
            tool_str = f"_for_{tool}"
        if status is None:
            status_str = ""
        else:
            status_str = f"_when_{status}"
        if all(map(lambda x: x is None, features)):
            features_str = ""
        else:
            features_str = "_using"
            if use_androguard:
                features_str += "_androguard"
            if use_java:
                features_str += "_java"
            if use_prolog:
                features_str += "_prolog"
            if use_ruby:
                features_str += "_ruby"
            if use_soot:
                features_str += "_soot"
            if use_apktool:
                features_str += "_apktool"
            if use_ocaml:
                features_str += "_ocaml"
            if use_python:
                features_str += "_python"
            if use_scala:
                features_str += "_scala"

        name = f"{limit}_most_common_errors_classes{tool_str}{status_str}{features_str}.csv"
        # make sure the folder exist
        folder.mkdir(parents=True, exist_ok=True)
        out = (folder / name).open("w")

    with sqlite3.connect(db) as con:
        cur = con.cursor()
        writer = csv.DictWriter(out, fieldnames=["type", "error", "count"])
        writer.writeheader()
        for row in cur.execute(
            (
                f"SELECT COUNT(*) AS cnt, distinct_error.error, distinct_error.error_type "
                f"FROM {DISTINCT_ERROR_CLASS} "
                "INNER JOIN tool ON distinct_error.tool_name = tool.tool_name "
                "INNER JOIN exec ON "
                "    distinct_error.tool_name = exec.tool_name AND "
                "    distinct_error.sha256 = exec.sha256 "
                f"{where_clause} "
                f"GROUP BY distinct_error.error, distinct_error.error_type "
                "ORDER BY cnt DESC LIMIT :limit;"
            ),
            args,
        ):
            row_d = {k: v for (k, v) in zip(("count", "error", "type"), row)}
            writer.writerow(row_d)
    if folder is not None:
        out.close()


def get_nb_error(
    db: Path,
    folder: Optional[Path] = None,
):
    NB_ERR = (
        "("
        "SELECT "
        "    exec_id.tool_name, exec_id.sha256, COUNT(error._rowid_) AS nb_err "
        "FROM ("
        "    (SELECT tool_name FROM tool) CROSS JOIN (SELECT sha256 FROM apk)"
        ") AS exec_id LEFT JOIN error "
        "ON exec_id.tool_name=error.tool_name AND exec_id.sha256=error.sha256 "
        "GROUP BY exec_id.tool_name, exec_id.sha256"
        ") AS nb_err"
    )
    data = {}
    tools = set()
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for tool, status, avg, variance in cur.execute(
            "SELECT nb_err.tool_name, exec.tool_status, AVG(nb_err.nb_err), "
            "    AVG(nb_err.nb_err*nb_err.nb_err) - AVG(nb_err.nb_err)*AVG(nb_err.nb_err) "
            f"FROM {NB_ERR} "
            "INNER JOIN exec ON nb_err.tool_name = exec.tool_name AND nb_err.sha256 = exec.sha256 "
            "GROUP BY nb_err.tool_name, exec.tool_status;"
        ):
            tools.add(tool)
            data[(tool, status)] = (avg, variance)
    fieldnames = list(tools)
    fieldnames.sort()
    fieldnames = ["", *fieldnames]
    if folder is None:
        fd = sys.stdout
    else:
        fd = (folder / "average_number_of_error_by_exec.csv").open("w")
    writer = csv.DictWriter(fd, fieldnames=fieldnames)
    writer.writeheader()
    for status in ("FINISHED", "FAILED", "TIMEOUT"):
        row = {"": status}
        for tool in tools:
            row[tool] = round(data.get((tool, status), (0, 0))[0], 2)
        writer.writerow(row)
        row = {"": "standard deviation"}
        for tool in tools:
            row[tool] = round(data.get((tool, status), (0, 0))[1] ** (1 / 2), 2)
        writer.writerow(row)
    if folder is not None:
        fd.close()


def error_type_repartition(
    db: Path, interactive: bool = True, folder: Optional[Path] = None
):
    data: dict[str, dict[str, int]] = {}
    total: dict[str, int] = {}
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        for tool, err, n in cur.execute(
            "SELECT tool_name, error, COUNT(*) FROM error GROUP BY tool_name, error;"
        ):
            if tool not in data:
                data[tool] = {}
                total[tool] = 0
            if err is not None and err != "":
                data[tool][err] = n
        for tool, n in cur.execute(
            "SELECT tool_name, COUNT(*) FROM error WHERE error IS NOT NULL AND error != '' GROUP BY tool_name;"
        ):
            total[tool] = n
    errors = set()
    N = 3
    for tool in data:
        for err in sorted(
            [err for err in data[tool]], key=lambda err: data[tool][err], reverse=True
        )[:N]:
            # TODO Check of > 10%?
            errors.add(err)
    tools = sorted(data.keys())
    errors_l = sorted(errors)
    values = [
        [
            data[tool].get(err, 0) * 100 / total[tool] if total[tool] != 0 else 0
            for tool in tools
        ]
        for err in errors_l
    ]
    plt.figure(figsize=(22, 20))
    im = plt.imshow(values, cmap="Greys")
    cbar = plt.colorbar(im)
    cbar.ax.set_ylabel(
        "% of the error type among the error raised by the tool",
        rotation=-90,
        va="bottom",
    )

    import numpy as np

    plt.xticks(np.arange(len(tools)), labels=tools, rotation=80)
    plt.yticks(np.arange(len(errors_l)), labels=errors_l)
    plt.xticks(np.arange(len(tools) + 1) - 0.5, minor=True)
    plt.yticks(np.arange(len(errors_l) + 1) - 0.5, minor=True)
    plt.grid(which="minor", color="w", linestyle="-", linewidth=3)
    plt.tick_params(which="minor", bottom=False, left=False)
    plt.title("Repartition of error types among tools")
    # plt.figure().set_figheight(10)
    render(
        "Repartition of error types among tools",
        interactive,
        folder,
        tight_layout=False,
    )
