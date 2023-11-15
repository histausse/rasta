"""
Plots related to the tool status.
"""

import numpy as np

import sqlite3
from pathlib import Path
from matplotlib import pyplot as plt  # type: ignore
from typing import Any, Callable, Optional
from .utils import (
    render,
    DENSE_DASH,
    DENSE_DOT,
    get_list_tools,
    plot_generic,
    MARKERS,
    COLORS,
)
from .populate_db_tool import TOOL_INFO

TOOL_LINE_STYLE = {
    tool_info["tool_name"]: DENSE_DOT if tool_info["use_soot"] else DENSE_DASH
    for tool_info in TOOL_INFO
}


def plot_status_by_tool(
    db: Path,
    interactive: bool = True,
    image_path: Path | None = None,
    tools: list[str] | None = None,
    title: str = "Exit Status",
):
    """Plot the repartition of status by tools."""
    if tools is None:
        tools = get_list_tools(db)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        tools_list_format = f"({','.join(['?' for _ in tools])})"
        nb_apk = cur.execute("SELECT COUNT(*) FROM apk;").fetchone()[0]
        status = cur.execute(
            (
                "SELECT tool_name, tool_status, COUNT(sha256) "
                "FROM exec "
                f"WHERE tool_name IN {tools_list_format}"
                "GROUP BY tool_name, tool_status;"
            ),
            tools,
        ).fetchall()
    occurences = {}
    for tool, stat, occurence in status:
        occurences[(tool, stat)] = occurence
    # tools.sort(key=lambda t: occurences.get((t, "FINISHED"), 0), reverse=True)
    tools.sort()

    values = {
        "Finished": np.zeros(len(tools)),
        "Time Out": np.zeros(len(tools)),
        "Other": np.zeros(len(tools)),
        "Failed": np.zeros(len(tools)),
    }
    colors = {
        "Finished": "#009E73",
        "Time Out": "#56B4E9",
        "Failed": "#D55E00",
        "Other": "#555555",  # TODO: better color
    }
    hatch = {
        "Finished": "/",
        "Time Out": "x",
        "Failed": "\\",
        "Other": ".",
    }
    for i, tool in enumerate(tools):
        values["Finished"][i] = occurences.get((tool, "FINISHED"), 0)
        values["Time Out"][i] = occurences.get((tool, "TIMEOUT"), 0)
        values["Failed"][i] = occurences.get((tool, "FAILED"), 0)
        values["Other"][i] = (
            nb_apk - values["Finished"][i] - values["Time Out"][i] - values["Failed"][i]
        )
    values["Finished"] = (100 * values["Finished"]) / nb_apk
    values["Time Out"] = (100 * values["Time Out"]) / nb_apk
    values["Failed"] = (100 * values["Failed"]) / nb_apk
    values["Other"] = (100 * values["Other"]) / nb_apk
    bottom = np.zeros(len(tools) * 2)
    bottom = np.zeros(len(tools))

    print("Finishing rate:")
    for t, p in zip(tools, values["Finished"]):
        print(f"{t}: {p:.2f}%")

    plt.figure(figsize=(20, 9), dpi=80)
    plt.axhline(y=50, linestyle="dotted")
    plt.axhline(y=85, linestyle="dotted")
    plt.axhline(y=15, linestyle="dotted")
    for stat in ["Finished", "Time Out", "Other", "Failed"]:
        plt.bar(
            tools,
            values[stat],
            label=stat,
            color=colors[stat],
            hatch=hatch[stat],
            bottom=bottom,
            width=0.6,
            edgecolor="black",
        )
        bottom += values[stat]
    plt.xticks(tools, tools, rotation=80)
    plt.legend()
    plt.ylabel("% of analysed apk")
    render(title, interactive, image_path)


def plot_status_by_tool_and_malware(
    db: Path,
    interactive: bool = True,
    image_path: Path | None = None,
    tools: list[str] | None = None,
    title: str = "Exit Status Goodware/Malware",
):
    """Plot the repartition of status by tools and if apk is a malware."""
    if tools is None:
        tools = get_list_tools(db)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        tools_list_format = f"({','.join(['?' for _ in tools])})"
        nb_goodware = cur.execute(
            "SELECT COUNT(*) FROM apk WHERE vt_detection == 0;"
        ).fetchone()[0]
        nb_malware = cur.execute(
            "SELECT COUNT(*) FROM apk WHERE vt_detection != 0;"
        ).fetchone()[0]
        status = cur.execute(
            (
                "SELECT tool_name, tool_status, COUNT(exec.sha256), vt_detection != 0 "
                "FROM exec INNER JOIN apk ON exec.sha256 = apk.sha256 "
                f"WHERE tool_name IN {tools_list_format} "
                "GROUP BY tool_name, tool_status, vt_detection != 0;"
            ),
            tools,
        ).fetchall()
    occurences = {}
    for tool, stat, occurence, malware in status:
        occurences[(tool, stat, bool(malware))] = occurence
    #    tools.sort(
    #        key=lambda t: occurences.get((t, "FINISHED", True), 0)
    #        + occurences.get((t, "FINISHED", False), 0),
    #        reverse=True,
    #    )
    tools.sort()

    values = {
        "Finished": np.zeros(len(tools) * 2),
        "Time Out": np.zeros(len(tools) * 2),
        "Other": np.zeros(len(tools) * 2),
        "Failed": np.zeros(len(tools) * 2),
    }
    colors = {
        "Finished": "#009E73",
        "Time Out": "#56B4E9",
        "Other": "#555555",  # TODO: find beter color
        "Failed": "#D55E00",
    }
    hatch = {
        "Finished": "/",
        "Time Out": "x",
        "Other": ".",
        "Failed": "\\",
    }
    for i, tool in enumerate(tools):
        i_goodware = 2 * i
        i_malware = 2 * i + 1
        values["Finished"][i_goodware] = occurences.get((tool, "FINISHED", False), 0)
        values["Finished"][i_malware] = occurences.get((tool, "FINISHED", True), 0)
        values["Time Out"][i_goodware] = occurences.get((tool, "TIMEOUT", False), 0)
        values["Time Out"][i_malware] = occurences.get((tool, "TIMEOUT", True), 0)
        values["Failed"][i_goodware] = occurences.get((tool, "FAILED", False), 0)
        values["Failed"][i_malware] = occurences.get((tool, "FAILED", True), 0)
        values["Other"][i_goodware] = (
            nb_goodware
            - values["Finished"][i_goodware]
            - values["Time Out"][i_goodware]
            - values["Failed"][i_goodware]
        )
        values["Other"][i_malware] = (
            nb_malware
            - values["Finished"][i_malware]
            - values["Time Out"][i_malware]
            - values["Failed"][i_malware]
        )
        values["Finished"][i_goodware] = (
            0
            if nb_goodware == 0
            else (100 * values["Finished"][i_goodware]) / nb_goodware
        )
        values["Finished"][i_malware] = (
            0 if nb_malware == 0 else (100 * values["Finished"][i_malware]) / nb_malware
        )
        values["Time Out"][i_goodware] = (
            0
            if nb_goodware == 0
            else (100 * values["Time Out"][i_goodware]) / nb_goodware
        )
        values["Time Out"][i_malware] = (
            0 if nb_malware == 0 else (100 * values["Time Out"][i_malware]) / nb_malware
        )
        values["Failed"][i_goodware] = (
            0
            if nb_goodware == 0
            else (100 * values["Failed"][i_goodware]) / nb_goodware
        )
        values["Failed"][i_malware] = (
            0 if nb_malware == 0 else (100 * values["Failed"][i_malware]) / nb_malware
        )
        values["Other"][i_goodware] = (
            0 if nb_goodware == 0 else (100 * values["Other"][i_goodware]) / nb_goodware
        )
        values["Other"][i_malware] = (
            0 if nb_malware == 0 else (100 * values["Other"][i_malware]) / nb_malware
        )
    bottom = np.zeros(len(tools) * 2)

    x_axis = np.zeros(len(tools) * 2)
    x_width = 3
    x_0 = x_width / 2
    lstep = 1
    bstep = 5
    for i in range(len(tools)):
        x_0 += bstep + x_width
        x_axis[2 * i] = x_0
        x_0 += lstep + x_width
        x_axis[2 * i + 1] = x_0
    tick_legend = []
    for tool in tools:
        tick_legend.append(f"{tool}")  # (f"{tool} on goodware")
        tick_legend.append("")  # (f"{tool} on malware")

    plt.figure(figsize=(20, 9), dpi=80)
    for stat in ["Finished", "Time Out", "Other", "Failed"]:
        plt.bar(
            x_axis,
            values[stat],
            label=stat,
            color=colors[stat],
            hatch=hatch[stat],
            bottom=bottom,
            width=x_width,
            edgecolor="black",
        )
        bottom += values[stat]
    plt.xticks(x_axis, tick_legend, rotation=80)
    plt.legend()
    plt.ylabel("% of analysed apk")
    render(title, interactive, image_path)


def plot_status_by_generic_x(
    tools: list[str],
    x_col: str,
    x_label: str,
    x_in_title: str,
    args,
    group_by: Optional[str] = None,
):
    tools.sort()
    """group_by default to x_col, x_col must be uniq for a grouped by group_by"""
    if group_by is None:
        group_by = x_col
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        nb_goodware_res = cur.execute(
            f"SELECT {group_by}, COUNT(*) FROM apk WHERE vt_detection == 0 GROUP BY {group_by};",
        ).fetchall()
        nb_goodware = {}
        for x_group, count in nb_goodware_res:
            nb_goodware[x_group] = count
        nb_malware_res = cur.execute(
            f"SELECT {group_by}, COUNT(*) FROM apk WHERE vt_detection != 0 GROUP BY {group_by};",
        ).fetchall()
        nb_malware = {}
        for x_group, count in nb_malware_res:
            nb_malware[x_group] = count
        statuses_res = cur.execute(
            (
                f"SELECT tool_name, {x_col}, {group_by}, COUNT(exec.sha256), vt_detection != 0 "
                "FROM exec INNER JOIN apk ON exec.sha256 = apk.sha256 "
                f"WHERE tool_status = 'FINISHED' "
                f"GROUP BY tool_name, tool_status, {group_by}, vt_detection != 0 "
                f"HAVING {x_col} IS NOT NULL;"
            )
        ).fetchall()
    tots = {}
    for tool_, x_val, x_group, count, is_malware in statuses_res:
        if not (tool_, x_group) in tots:
            tots[(tool_, x_group)] = [x_val, 0]
        tots[(tool_, x_group)][1] += count
    plots = []
    plots_malgood = []
    metas = []
    metas_malgood = []
    for tool in tools:
        malware_plot = [
            (x_val, 100 * count / nb_malware[x_group])
            for (tool_, x_val, x_group, count, is_malware) in statuses_res
            if (tool_ == tool) and is_malware and nb_malware.get(x_group, 0) != 0
        ]
        malware_meta = (f"{tool} on malware", DENSE_DOT, MARKERS[tool], COLORS[tool])
        goodware_plot = [
            (x_val, 100 * count / nb_goodware[x_group])
            for (tool_, x_val, x_group, count, is_malware) in statuses_res
            if (tool_ == tool) and not is_malware and nb_goodware.get(x_group, 0) != 0
        ]
        goodware_meta = (f"{tool} on goodware", DENSE_DASH, MARKERS[tool], COLORS[tool])
        total_plot = [
            (
                x_val,
                100
                * count
                / (nb_malware.get(x_group, 0) + nb_goodware.get(x_group, 0)),
            )
            for ((tool_, x_group), (x_val, count)) in tots.items()
            if (tool_ == tool)
            and (nb_malware.get(x_group, 0) + nb_goodware.get(x_group, 0)) != 0
        ]
        total_meta = (f"{tool}", DENSE_DOT, MARKERS[tool], COLORS[tool])
        plots.append(total_plot)
        plots_malgood.append(malware_plot)
        plots_malgood.append(goodware_plot)
        metas.append(total_meta)
        metas_malgood.append(malware_meta)
        metas_malgood.append(goodware_meta)

        plot_generic(
            [goodware_plot, malware_plot],
            [goodware_meta, malware_meta],
            x_label,
            "finishing rate",
            f"Finishing Rate by {x_in_title} for {tool} on malware and goodware",
            ylim=(-5, 105),
            interactive=args.display,
            image_path=args.figures_file,
        )
        plot_generic(
            [total_plot],
            [total_meta],
            x_label,
            "finishing rate",
            f"Finishing Rate by {x_in_title} for {tool}",
            ylim=(-5, 105),
            interactive=args.display,
            image_path=args.figures_file,
        )
    plot_generic(
        plots_malgood,
        metas_malgood,
        x_label,
        "finishing rate",
        f"Finishing Rate by {x_in_title} on malware and goodware",
        ylim=(-5, 105),
        interactive=args.display,
        image_path=args.figures_file,
    )
    plot_generic(
        plots,
        metas,
        x_label,
        "finishing rate",
        f"Finishing Rate by {x_in_title}",
        ylim=(-5, 105),
        interactive=args.display,
        image_path=args.figures_file,
    )


def dbg(arg):
    # print(arg)
    return arg


def plot_all_status_by_generic_x(
    tools: list[str],
    x_col: str,
    x_label: str,
    title: str,
    args,
    condition: Optional[str] = None,
    apk_condition: Optional[str] = None,
    group_by: Optional[str] = None,
):
    if condition is None and apk_condition is None:
        condition = ""
        apk_condition = ""
    elif apk_condition is None:
        condition = f"AND ({condition})"
        apk_condition = ""
    elif condition is None:
        condition = f"AND ({apk_condition})"
        apk_condition = f"WHERE ({apk_condition})"
    else:
        condition = f"AND ({apk_condition}) AND ({condition})"
        apk_condition = f"WHERE ({apk_condition})"
    if group_by is None:
        group_by = x_col
    nb_apk = {}
    tools.sort()
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        for x_group, count in cur.execute(
            f"SELECT {group_by}, COUNT(*) FROM apk {apk_condition} GROUP BY {group_by};",
        ):
            nb_apk[x_group] = count
        statuses_res = cur.execute(
            dbg(
                f"SELECT exec.tool_name, {x_col}, {group_by}, COUNT(exec.sha256) "
                "FROM exec "
                "    INNER JOIN apk ON exec.sha256 = apk.sha256 "
                "    INNER JOIN tool ON exec.tool_name = tool.tool_name "
                f"WHERE tool_status = 'FINISHED' {condition} "
                f"GROUP BY exec.tool_name, tool_status, {group_by} "
                f"HAVING {x_col} IS NOT NULL;"
            )
        ).fetchall()
    plots = []
    metas = []
    for tool in tools:
        plot = [
            (x_val, 100 * count / nb_apk[x_group])
            for (tool_, x_val, x_group, count) in statuses_res
            if (tool_ == tool) and nb_apk.get(x_group, 0) != 0
        ]
        if len(plot) == 0:
            continue
        meta = (tool, TOOL_LINE_STYLE[tool], MARKERS[tool], COLORS[tool])
        plots.append(plot)
        metas.append(meta)
    plot_generic(
        plots,
        metas,
        x_label,
        "finishing rate",
        title,
        ylim=(-5, 105),
        interactive=args.display,
        image_path=args.figures_file,
    )
