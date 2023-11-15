import argparse
import code
import json
import sys
import sqlite3

import seaborn as sns  # type: ignore

sns.set_context("talk")

from pathlib import Path
from math import floor, log
from typing import Callable, Any

from .status import (
    plot_status_by_tool,
    plot_status_by_tool_and_malware,
    plot_all_status_by_generic_x,
    plot_status_by_generic_x,
)
from .apk import (
    plot_apk_info_by_generic_x,
    plot_apk_size,
    plot_apk_size_hl_subset,
)
from .populate_db_apk import populate_db_apk as populate_db_apk_
from .utils import (
    mean,
    median,
    get_list_tools,
    DENSE_DASH,
    DENSE_DOT,
)
from .ressources import get_ressource
from .populate_db_exec import (
    populate_execution_report,
    fix_error,
    estimate_cause,
)
from .populate_db_tool import populate_tool
from .query_error import (
    get_common_errors,
    get_common_error_classes,
    get_nb_error,
    radar_cause_estimation,
    error_type_repartition,
)
from .ic3 import ic3_venn, ic3_errors
from .data_set import gen_dataset


def round_apk_size(size) -> float:
    return 4 ** floor(log(size, 4))


def get_common_arg(description: str = "") -> argparse.ArgumentParser:
    """Get the usual arguments."""
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=description)
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database that contain the execution report and apk info",
    )
    parser.add_argument(
        "-f",
        "--figures-file",
        type=Path,
        help="The folder in which the figures must be stored",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="If the figures must be displayed",
    )
    parser.add_argument(
        "-t",
        "--tools",
        nargs="+",
        default=None,
        help="The tools to analyse",
    )

    return parser


def main():
    """Console entrypoint."""
    show_status_by_tool()
    show_success_rate_by_first_seen_year()
    show_success_rate_by_size_decile()
    show_success_rate_by_min_sdk()
    show_success_rate_by_target_sdk()
    show_success_rate_by_dex_size()


#    show_timeout_rate_by_estimated_year()
#    show_timeout_rate_by_dex_size()
#    show_timeout_rate_by_target_sdk()
#    show_timeout_rate_by_min_sdk()
#    show_data_set_relations()
#    show_mem_by_dex_size()
#    show_mem_by_min_sdk()
#    show_mem_by_target_sdk()
#    show_mem_by_estimated_year()
#    show_time_by_dex_size()
#    show_time_by_min_sdk()
#    show_time_by_target_sdk()
#    show_time_by_estimated_year()


def show_status_by_tool():
    """Display the repartition of status by tool."""
    parser = get_common_arg("Display the repartition of status by tool")
    parser.add_argument(
        "--title",
        default="Exit Status",
        help="The title of the graph",
    )
    args = parser.parse_args()

    plot_status_by_tool(
        args.data,
        interactive=args.display,
        image_path=args.figures_file,
        tools=args.tools,
        title=args.title,
    )
    plot_status_by_tool_and_malware(
        args.data,
        interactive=args.display,
        image_path=args.figures_file,
        tools=args.tools,
        title=f"{args.title} Goodware/Malware",
    )


def show_success_rate_by_first_seen_year():
    args = get_common_arg(
        "Plot success rate by the first year they were seen"
    ).parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    plot_status_by_generic_x(
        tools, "first_seen_year", "first seen year", "App First Year Seen", args
    )
    plot_all_status_by_generic_x(
        tools,
        "first_seen_year",
        "first seen year",
        "Finishing Rate by Year of Java based tools",
        args,
        condition="tool.use_java = TRUE",
    )
    plot_all_status_by_generic_x(
        tools,
        "first_seen_year",
        "first seen year",
        "Finishing Rate by Year of Non Java based tools",
        args,
        condition="tool.use_java = FALSE",
    )


def show_success_rate_by_size_decile():
    args = get_common_arg("Plot success rate by the size of the apk").parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    plot_status_by_generic_x(
        tools,
        "MAX(apk_size)/1000000",
        "apk size (MB)",
        "APK Size",
        args,
        group_by="apk_size_decile",
    )  # TODO bleurk those names...
    plot_all_status_by_generic_x(
        tools,
        "MAX(apk_size)/1000000",
        "apk size (MB)",
        "Finishing Rate by APK size for tools using java",
        args,
        condition="tool.use_java = TRUE",
        group_by="apk_size_decile",
    )
    plot_all_status_by_generic_x(
        tools,
        "MAX(apk_size)/1000000",
        "apk size (MB)",
        "Finishing Rate by APK size for tools not using java",
        args,
        condition="tool.use_java = FALSE",
        group_by="apk_size_decile",
    )


def show_success_rate_by_min_sdk():
    args = get_common_arg("Plot success rate by min sdk").parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    # plot_status_by_generic_x(tools, "min_sdk", "min SDK", "Min SDK", args)
    plot_all_status_by_generic_x(
        tools,
        "min_sdk",
        "min SDK",
        "Finishing Rate by min SDK version for tools using java",
        args,
        condition="tool.use_java = TRUE",
    )
    plot_all_status_by_generic_x(
        tools,
        "min_sdk",
        "min SDK",
        "Finishing Rate by min SDK version for tools not using java",
        args,
        condition="tool.use_java = FALSE",
    )


def show_success_rate_by_target_sdk():
    args = get_common_arg("Plot success rate by target sdk").parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    plot_status_by_generic_x(tools, "target_sdk", "target SDK", "Target SDK", args)
    plot_all_status_by_generic_x(
        tools,
        "target_sdk",
        "target SDK",
        "Finishing Rate by target SDK version for tools using java",
        args,
        condition="tool.use_java = TRUE",
    )
    plot_all_status_by_generic_x(
        tools,
        "target_sdk",
        "target SDK",
        "Finishing Rate by target SDK version for tools not using java",
        args,
        condition="tool.use_java = FALSE",
    )


def show_success_rate_by_dex_size():
    args = get_common_arg("Plot success rate by size of bytecode").parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    plot_status_by_generic_x(
        tools,
        "MAX(dex_size)/1000",
        "bytecode size (KB)",
        "bytecode Size",
        args,
        group_by="dex_size_decile",
    )  # TODO bleurk those names...
    plot_all_status_by_generic_x(
        tools,
        "MAX(dex_size)/1000",
        "bytecode size (KB)",
        "Finishing Rate by bytecode size for tools using java",
        args,
        condition="tool.use_java = TRUE",
        group_by="dex_size_decile",
    )
    plot_all_status_by_generic_x(
        tools,
        "MAX(dex_size)/1000",
        "dex size (KB)",
        "Finishing Rate by bytecode size for tools not using java",
        args,
        condition="tool.use_java = FALSE",
        group_by="dex_size_decile",
    )


def populate_db_apk():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Populate a sqlite3 database with informationn abouts the apks of the dataset",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database to populate",
    )
    parser.add_argument(
        "-a",
        "--apks",
        type=Path,
        help="The file listing the apks sha256",
    )
    parser.add_argument(
        "--year-and-sdk",
        type=Path,
        help="The path to year_and_sdk.csv.gz",
    )
    parser.add_argument(
        "--latest-with-added-date",
        type=Path,
        help="The path to latest_with-added-date.csv.gz",
    )
    parser.add_argument(
        "--fix-dex-file",
        action="store_true",
        help=(
            "If the dex_file column must be set by the sum of all .dex files size "
            "(long operation, need to actually download the apks)"
        ),
    )
    args = parser.parse_args()
    populate_db_apk_(
        args.data,
        args.apks,
        args.year_and_sdk,
        args.latest_with_added_date,
        args.fix_dex_file,
    )


def populate_db_exec():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Populate a sqlite3 database with the execution reports",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database to populate",
    )
    parser.add_argument(
        "-r",
        "--reports",
        type=Path,
        default=None,
        help="The folder containing the execution reports",
    )
    parser.add_argument(
        "--substitue-error",
        action="store_true",
        help=(
            "If the report should be used to substitute the errors of already populated "
            "entry (to fix the parsing error)"
        ),
    )
    parser.add_argument(
        "--estimate-cause",
        action="store_true",
        help=(
            "If the cause of the errors must be estimated after populating the DB "
            "(operation on all entries of the error table)"
        ),
    )

    args = parser.parse_args()
    if not args.substitue_error and args.reports is not None:
        populate_execution_report(
            args.data,
            args.reports,
        )
    elif args.reports and args.reports is not None:
        fix_error(args.data, args.reports)
    if args.estimate_cause:
        estimate_cause(args.data)


def populate_db_tool():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Populate a sqlite3 database with the tool information",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database to populate",
    )
    args = parser.parse_args()
    populate_tool(
        args.data,
    )


def show_common_errors():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Find the most common errors matching given criterions",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database containing the results",
    )
    parser.add_argument(
        "-n",
        "--nb-errors",
        type=int,
        default=10,
        help="the number of errors to find",
    )
    parser.add_argument(
        "-t",
        "--tool",
        default=None,
        help="restrict the error to the one raised by a specific tool",
    )
    parser.add_argument(
        "-s",
        "--status",
        default=None,
        help="restrict the error to the one raised when the tool FAILED, FINISHED, or TIMEOUT",
    )
    for carac in [
        "androguard",
        "java",
        "prolog",
        "ruby",
        "soot",
        "apktool",
        "ocaml",
        "python",
        "scala",
    ]:
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            f"--use-{carac}",
            action="store_true",
            help=(f"restrict the error to the one raised by tool that use {carac}"),
        )
        group.add_argument(
            f"--dont-use-{carac}",
            action="store_true",
            help=(
                f"restrict the error to the one raised by tool that do not use {carac}"
            ),
        )

    parser.add_argument(
        "-f",
        "--folder",
        type=Path,
        help="The folder in which the csv must be stored",
    )

    args = parser.parse_args()
    carac_kargs = {}
    for carac in [
        "androguard",
        "java",
        "prolog",
        "ruby",
        "soot",
        "apktool",
        "ocaml",
        "python",
        "scala",
    ]:
        if vars(args)[f"use_{carac}"]:
            carac_kargs[f"use_{carac}"] = True
        if vars(args)[f"dont_use_{carac}"]:
            carac_kargs[f"use_{carac}"] = False

    if args.folder is None:
        print("Error:")
    get_common_errors(
        args.data,
        tool=args.tool,
        status=args.status,
        limit=args.nb_errors,
        folder=args.folder,
        **carac_kargs,
    )
    if args.folder is None:
        print("-" * 30)
        print("Error classes:")
    get_common_error_classes(
        args.data,
        tool=args.tool,
        status=args.status,
        limit=args.nb_errors,
        folder=args.folder,
        **carac_kargs,
    )

    if args.tool is None:
        for tool in get_list_tools(args.data):
            if args.folder is None:
                print("-" * 30)
                print(f"Top {args.nb_errors} errors for {tool}:")
            get_common_errors(
                args.data,
                tool=tool,
                status=args.status,
                limit=args.nb_errors,
                folder=args.folder,
                **carac_kargs,
            )

    if args.tool is None:
        for tool in get_list_tools(args.data):
            if args.folder is None:
                print("-" * 30)
                print(f"Top {args.nb_errors} error classes for {tool}:")
            get_common_error_classes(
                args.data,
                tool=tool,
                status=args.status,
                limit=args.nb_errors,
                folder=args.folder,
                **carac_kargs,
            )


def show_error_avg_occ_by_exec():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Compute average number of occurences in an exec for an error",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database containing the results",
    )
    parser.add_argument(
        "-e",
        "--error",
        required=True,
        type=str,
        help="The error to count",
    )
    args = parser.parse_args()
    print_avg_occ_in_exec(args.data, args.error)


def ic3():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Analyse the executions of ic3 and ic3_fork",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database containing the results",
    )
    parser.add_argument(
        "-f",
        "--figures-file",
        type=Path,
        help="The folder in which the figures must be stored",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="If the figures must be displayed",
    )
    args = parser.parse_args()
    ic3_venn(args.data, interactive=args.display, image_path=args.figures_file)
    ic3_errors(
        args.data,
        file=args.figures_file / "ic3_err.csv"
        if args.figures_file is not None
        else None,
    )


def show_error_cause_radar():
    parser = get_common_arg(
        "Compute radar charts that show common identifiable causes of crash"
    )
    args = parser.parse_args()
    radar_cause_estimation(args.data, args.tools, args.display, args.figures_file)


def average_nb_errors():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Compute the average number of error by execution",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database containing the results",
    )
    parser.add_argument(
        "-f",
        "--figures-file",
        type=Path,
        help="The folder result must be stored",
    )
    args = parser.parse_args()
    get_nb_error(args.data, args.figures_file)


def show_error_type_repartition():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Compute a heat map of error type repartition by tool",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database containing the results",
    )
    parser.add_argument(
        "-f",
        "--figures-file",
        type=Path,
        help="The folder in which the figures must be stored",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="If the figures must be displayed",
    )
    args = parser.parse_args()
    error_type_repartition(args.data, args.display, args.figures_file)


def show_apk_year_repartition_by_decil():
    args = get_common_arg("Test").parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools
    import sqlite3
    import matplotlib.pyplot as plt  # type: ignore

    deciles = [{} for _ in range(11)]
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        for d, y, n in cur.execute(
            "SELECT dex_size_decile, first_seen_year, COUNT(*) FROM apk GROUP BY dex_size_decile, first_seen_year;"
        ):
            deciles[d][y] = n
    fig, axes = plt.subplots(3, 4)
    fig.set_size_inches((24, 12))
    for d in range(1, 11):
        years = sorted(deciles[d].keys())
        ax = axes[(d - 1) % 3, (d - 1) // 3]
        ax.bar(
            years,
            [deciles[d][y] for y in years],
            edgecolor="black",
        )
        ax.legend()
        ax.set_title(f"Decile {d}")
    plt.show()
    # Size dispertion inside decile
    # SELECT dex_size_decile, (100*(MAX(dex_size) - MIN (dex_size)))/AVG(dex_size) FROM apk GROUP BY dex_size_decile;
    # SELECT dex_size_decile, (MAX(dex_size) - MIN (dex_size)) FROM apk GROUP BY dex_size_decile;
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        for d, m, v in cur.execute(
            "SELECT dex_size_decile, AVG(dex_size), AVG(dex_size*dex_size) - AVG(dex_size)*AVG(dex_size) "
            "FROM apk GROUP BY dex_size_decile "
            "ORDER BY dex_size_decile;"
        ):
            m = round(m / 1024 / 1024, 2)
            s = round(v * 0.5 / 1024 / 1024, 2)
            print(f"Decile {d}: moyenne: {m} MB, ecart type: {s} MB")


def plot_decorelated_factor():
    parser = get_common_arg("Plot graph while fixing to parameter to decorelate them")
    parser.add_argument(
        "--decile",
        default=8,
        type=int,
        help="The decile to use for fixed size result",
    )
    args = parser.parse_args()
    if args.tools is None:
        tools = get_list_tools(args.data)
    else:
        tools = args.tools

    plot_all_status_by_generic_x(
        tools,
        "(SELECT AVG(apk2.dex_size)/1000000 FROM apk AS apk2 WHERE apk2.dex_size_decile_by_year = apk.dex_size_decile_by_year AND apk2.first_seen_year = 2022)",
        "bytecode size (MB)",
        "Finishing Rate of java based tool by bytecode size of apks detected in 2022",
        args,
        condition="tool.use_java = TRUE",
        apk_condition="apk.first_seen_year = 2022",
        group_by="dex_size_decile_by_year",
    )
    plot_all_status_by_generic_x(
        tools,
        "(SELECT AVG(apk2.dex_size)/1000000 FROM apk AS apk2 WHERE apk2.dex_size_decile_by_year = apk.dex_size_decile_by_year AND apk2.first_seen_year = 2022)",
        "bytecode size (MB)",
        "Finishing Rate of non-java based tool by bytecode size of apks detected in 2022",
        args,
        condition="tool.use_java = FALSE",
        apk_condition="apk.first_seen_year = 2022",
        group_by="dex_size_decile_by_year",
    )

    MIN_YEAR = [None, 2010, 2010, 2011, 2012, 2013, 2013, 2014, 2015, 2016, 2019]
    MAX_YEAR = [None, 2017, 2017, 2024, 2024, 2024, 2024, 2024, 2024, 2024, 2024]
    import sqlite3

    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        min_size, max_size = cur.execute(
            "SELECT MIN(dex_size), MAX(dex_size) "
            "FROM apk WHERE dex_size_decile = ?;",
            (args.decile,),
        ).fetchone()
    min_size = round(min_size / 1024 / 1024, 2)
    max_size = round(max_size / 1024 / 1024, 2)

    plot_all_status_by_generic_x(
        tools,
        "apk.first_seen_year",
        "Year",
        (
            "Finishing Rate of java based tool by discovery year of apks with a bytecode "
            f"size between {min_size} MB and {max_size} MB"
        ),
        args,
        condition="tool.use_java = TRUE",
        apk_condition=(
            f"apk.dex_size_decile = {args.decile} AND "
            f"apk.first_seen_year >= {MIN_YEAR[args.decile]} AND "
            f"apk.first_seen_year <= {MAX_YEAR[args.decile]}"
        ),
    )
    plot_all_status_by_generic_x(
        tools,
        "apk.first_seen_year",
        "Year",
        (
            "Finishing Rate of non-java based tool by discovery year of apks with a bytecode "
            f"size between {min_size} MB and {max_size} MB"
        ),
        args,
        condition="tool.use_java = FALSE",
        apk_condition=(
            f"apk.dex_size_decile = {args.decile} AND "
            f"apk.first_seen_year >= {MIN_YEAR[args.decile]} AND "
            f"apk.first_seen_year <= {MAX_YEAR[args.decile]}"
        ),
    )

    plot_all_status_by_generic_x(
        tools,
        "apk.min_sdk",
        "Min SDK",
        (
            "Finishing Rate of java based tool by min SDK of apks with a bytecode "
            f"size between {min_size} MB and {max_size} MB"
        ),
        args,
        condition="tool.use_java = TRUE",
        apk_condition=(
            f"apk.dex_size_decile = {args.decile} AND "
            f"apk.first_seen_year >= {MIN_YEAR[args.decile]} AND "
            f"apk.first_seen_year <= {MAX_YEAR[args.decile]}"
        ),
    )
    plot_all_status_by_generic_x(
        tools,
        "apk.min_sdk",
        "Min SDK",
        (
            "Finishing Rate of non-java based tool by min SDK of apks with a bytecode "
            f"size between {min_size} MB and {max_size} MB"
        ),
        args,
        condition="tool.use_java = FALSE",
        apk_condition=(
            f"apk.dex_size_decile = {args.decile} AND "
            f"apk.first_seen_year >= {MIN_YEAR[args.decile]} AND "
            f"apk.first_seen_year <= {MAX_YEAR[args.decile]}"
        ),
    )

    plot_all_status_by_generic_x(
        tools,
        "(SELECT AVG(apk2.dex_size)/1000000 FROM apk AS apk2 WHERE apk2.dex_size_decile = apk.dex_size_decile AND apk2.min_sdk = 16)",
        "bytecode size (MB)",
        "Finishing Rate of java based tool by bytecode size of apks with min SDK = 16",
        args,
        condition="tool.use_java = TRUE",
        apk_condition="apk.min_sdk = 16",
        group_by="dex_size_decile",
    )
    plot_all_status_by_generic_x(
        tools,
        "(SELECT AVG(apk2.dex_size)/1000000 FROM apk AS apk2 WHERE apk2.dex_size_decile = apk.dex_size_decile AND apk2.min_sdk = 16)",
        "bytecode size (MB)",
        "Finishing Rate of non java based tool by bytecode size of apks with min SDK = 16",
        args,
        condition="tool.use_java = FALSE",
        apk_condition="apk.min_sdk = 16",
        group_by="dex_size_decile",
    )


def get_avg_ressource_consumption():
    parser = get_common_arg("Compute the average ressource consumption of the tools")
    args = parser.parse_args()
    get_ressource(args.data, args.figures_file)


def rate_malware_decile():
    parser = get_common_arg("Test")
    args = parser.parse_args()
    import sqlite3

    tot_size_good = None
    tot_size_mal = None
    size_good = [0 for _ in range(11)]
    size_mal = [0 for _ in range(11)]
    tot_sd_good = None
    tot_sd_mal = None
    sd_good = [0 for _ in range(11)]
    sd_mal = [0 for _ in range(11)]
    nb_apk_good = [0 for _ in range(11)]
    nb_apk_mal = [0 for _ in range(11)]
    nb_success_good = [0 for _ in range(11)]
    nb_success_mal = [0 for _ in range(11)]
    NB_TOOL = 20
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        for is_good, decile, n, m, v in cur.execute(
            "SELECT vt_detection = 0, dex_size_decile, COUNT(*), "
            "    AVG(dex_size), AVG(dex_size*dex_size) - AVG(dex_size)*AVG(dex_size) "
            "FROM apk GROUP BY vt_detection = 0, dex_size_decile;",
        ):
            if is_good:
                nb_apk_good[decile] = n
                size_good[decile] = round(m / 1024 / 1024, 2)
                sd_good[decile] = round(v ** (1 / 2) / 1024 / 1024, 2)
            else:
                nb_apk_mal[decile] = n
                size_mal[decile] = round(m / 1024 / 1024, 2)
                sd_mal[decile] = round(v ** (1 / 2) / 1024 / 1024, 2)
        for is_good, m, v in cur.execute(
            "SELECT vt_detection = 0, AVG(dex_size), AVG(dex_size*dex_size) - AVG(dex_size)*AVG(dex_size) "
            "FROM apk GROUP BY vt_detection = 0",
        ):
            if is_good:
                tot_size_good = round(m / 1024 / 1024, 2)
                tot_sd_good = round(v ** (1 / 2) / 1024 / 1024, 2)
            else:
                tot_size_mal = round(m / 1024 / 1024, 2)
                tot_sd_mal = round(v ** (1 / 2) / 1024 / 1024, 2)

        for is_good, decile, n in cur.execute(
            "SELECT vt_detection = 0, dex_size_decile, COUNT(*) "
            "FROM exec INNER JOIN apk ON exec.sha256 = apk.sha256 "
            "WHERE tool_status = 'FINISHED' "
            "GROUP BY vt_detection = 0, dex_size_decile;",
        ):
            if is_good:
                nb_success_good[decile] = n
            else:
                nb_success_mal[decile] = n
    tot_apk_good = sum(nb_apk_good)

    tot_apk_mal = sum(nb_apk_mal)
    tot_success_good = sum(nb_success_good)
    tot_success_mal = sum(nb_success_mal)

    print(
        "             rate goodware    rate malware     avg size goodware (MB)    avg size malware (MB)"
    )
    for d in range(1, 11):
        rate_good = round(nb_success_good[d] / nb_apk_good[d] / NB_TOOL * 100, 2)
        rate_mal = round(nb_success_mal[d] / nb_apk_mal[d] / NB_TOOL * 100, 2)
        print(
            f"decile {d: >2}: {rate_good: >15} {rate_mal: >15} {size_good[d]: >26} {size_mal[d]: >24}"
        )
    rate_good = round(tot_success_good / tot_apk_good / NB_TOOL * 100, 2)
    rate_mal = round(tot_success_mal / tot_apk_mal / NB_TOOL * 100, 2)
    print(
        f"total:     {rate_good: >15} {rate_mal: >15} {tot_size_good: >26} {tot_size_mal: >24}"
    )


def count_error_stacks():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=(
            "Read a list of report file in stdin and extract and sort "
            "by occurences the error stack that match the parameters.\n"
            "The list can be generated with find_apks_by_tool_error.sh: \n"
            "    `./find_apks_by_tool_error.sh androguard_dad OSError rasta.db | rasta-count-error-stacks -e OSError`"
        ),
    )
    parser.add_argument(
        "-e",
        "--error",
        required=True,
        help="The error type to studdy",
    )
    parser.add_argument(
        "-m",
        "--msg",
        required=False,
        default=None,
        help="The error msg to studdy",
    )
    parser.add_argument(
        "-s",
        "--status",
        required=False,
        default=None,
        choices=["FAILED", "FINISHED", "TIMEOUT"],
        help="Restrict the search to the tool that exited with a specific status",
    )
    args = parser.parse_args()
    import json

    stacks = {}
    while True:
        try:
            file = input()
        except EOFError:
            break
        with open(file) as fp:
            report = json.load(fp)
        if args.status is not None and report.get("tool-status", None) != args.status:
            continue
        for err in report["errors"]:
            if (
                "error" in err
                and err["error"] == args.error
                and (args.msg is None or ("msg" in err and err["msg"] == args.msg))
            ):
                k = json.dumps(err["stack"], indent="  ")
                if k not in stacks:
                    stacks[k] = 0
                stacks[k] += 1
    keys = sorted(stacks.keys(), key=lambda k: stacks[k])
    for k in keys:
        print(f"{k}: {stacks[k]} occurences")


def generate_dataset():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Generate a dataset from androzoo list. The default values are the one used for the RASTA dataset",
    )
    parser.add_argument(
        "latest",
        type=Path,
        help="latest.csv.gz, the list of apk from androzoo",
    )
    parser.add_argument(
        "year_sdk_csv",
        type=Path,
        help="year_and_sdk.csv.gz, the list of apk from androzoo with the pulication year and sdk version",
    )
    parser.add_argument(
        "--out",
        "-o",
        required=False,
        type=Path,
        default=Path(".") / "rasta_dataset",
        help="Where to store the dataset",
    )
    parser.add_argument(
        "-s",
        "--random_seed",
        required=False,
        default=1234567890,
        type=int,
        help="The seed to use for the random generator",
    )
    parser.add_argument(
        "-n",
        "--nb_sub_dataset",
        required=False,
        default=10,
        type=int,
        help="The number of subdatasets",
    )
    parser.add_argument(
        "-ns",
        "--nb_apk_by_bucket_by_subset",
        default=50,
        type=int,
        help="The number of apk in each size bucket of each subset",
    )
    parser.add_argument(
        "-mp",
        "--proportion_malware",
        default=0.07,
        type=float,
        help="The proportion of malware in the dataset",
    )
    parser.add_argument(
        "-vt",
        "--vt_threshold",
        default=5,
        type=int,
        help="The number of virustotal detection from which we considere an apk to be a malware",
    )
    parser.add_argument(
        "-nq",
        "--nb_size_quantile",
        default=10,
        type=int,
        help="The number of quantile to use for the size of the apk",
    )
    parser.add_argument(
        "-ex",
        "--exclution_prop",
        default=0.01,
        type=float,
        help="The proportion of apk to exclude at each size extreme",
    )
    parser.add_argument(
        "-my",
        "--min_year",
        default=2010,
        type=int,
        help="The min year of the year range",
    )
    parser.add_argument(
        "-My",
        "--max_year",
        default=2023,
        type=int,
        help="The max year of the year range",
    )

    args = parser.parse_args()

    gen_dataset(
        args.latest,
        args.year_sdk_csv,
        args.out,
        nb_sub_dataset=args.nb_sub_dataset,
        nb_apk_by_bucket_by_subset=args.nb_apk_by_bucket_by_subset,
        proportion_malware=args.proportion_malware,
        vt_threshold=args.vt_threshold,
        nb_bucket=args.nb_size_quantile,
        exclution=args.exclution_prop,
        min_year=args.min_year,
        max_year=args.max_year,
        random_seed=args.random_seed,
    )


def size_malware():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Compare size and success rate proportion for malwares and goodware",
    )
    parser.add_argument(
        "-d",
        "--data",
        required=True,
        type=Path,
        help="The sqlite3 database that contain the execution report and apk info",
    )
    args = parser.parse_args()

    nb_tool = len(get_list_tools(args.data))
    nb_apk = {}
    size_apk = {}
    nb_finished = {}
    with sqlite3.connect(args.data) as con:
        cur = con.cursor()
        for decile, is_goodware, n, avg_size in cur.execute(
            "SELECT dex_size_decile, vt_detection = 0, COUNT(*), AVG(dex_size) FROM apk GROUP BY dex_size_decile, vt_detection = 0;"
        ):
            nb_apk[(decile, bool(is_goodware))] = n
            size_apk[(decile, bool(is_goodware))] = avg_size
        for is_goodware, n, avg_size in cur.execute(
            "SELECT vt_detection = 0, COUNT(*), AVG(dex_size) FROM apk GROUP BY vt_detection = 0;"
        ):
            nb_apk[("total", bool(is_goodware))] = n
            size_apk[("total", bool(is_goodware))] = avg_size
        for decile, is_goodware, n in cur.execute(
            "SELECT dex_size_decile, vt_detection = 0, COUNT(*) "
            "FROM exec INNER JOIN apk ON apk.sha256=exec.sha256 "
            "WHERE tool_status = 'FINISHED' OR tool_status = 'OTHER' "
            "GROUP BY dex_size_decile, vt_detection = 0;"
        ):
            nb_finished[(decile, bool(is_goodware))] = n
        for is_goodware, n in cur.execute(
            "SELECT vt_detection = 0, COUNT(*) "
            "FROM exec INNER JOIN apk ON apk.sha256=exec.sha256 "
            "WHERE tool_status = 'FINISHED' OR tool_status = 'OTHER' "
            "GROUP BY vt_detection = 0;"
        ):
            nb_finished[("total", bool(is_goodware))] = n

    print(
        "dex size decile, average size goodware, average size malware, finishing rate goodware, finishing rate malware, average size goodware/malware, finishing rate goodware/malware"
    )
    for size in ["total", *range(1, 11)]:
        finishing_rate_goodware = nb_finished[(size, True)] / (
            nb_tool * nb_apk[(size, True)]
        )
        finishing_rate_malware = nb_finished[(size, False)] / (
            nb_tool * nb_apk[(size, False)]
        )
        print(
            f"{size}, {size_apk[(size, True)]:.2f}, {size_apk[(size, False)]:.2f}, {finishing_rate_goodware:.2f}, {finishing_rate_malware:.2f}, {size_apk[(size, True)] / size_apk[(size, False)]:.2f}, {finishing_rate_goodware/finishing_rate_malware:.2f}"
        )
