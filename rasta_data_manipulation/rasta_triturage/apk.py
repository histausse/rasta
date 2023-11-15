"""
Collect data about apks.
"""

import dateutil.parser as dp  # type: ignore
import datetime
import numpy as np
import matplotlib.pyplot as plt  # type: ignore

from typing import Any, IO, Callable
from pathlib import Path

from .utils import render


def plot_apk_info_by_generic_x(
    data: list[Any],
    x: str,
    title: str,
    extract_propertie: Callable,
    y_label: str,
    x_label: str | None = None,
    reductions: dict[str, Callable] | None = None,
    xscale: str = "linear",
    interactive: bool = True,
    image_path: Path | None = None,
):
    """`extract_propertie` is a founction that take a list of element and return
    a value representing the value of the list, like a median or a mean.
    """
    raise NotImplementedError("TODO: update function to use sqlite3")


#    groupped = group_by(x, data, reductions=reductions)
#    properties = {k: extract_propertie(v) for k, v in groupped.items()}
#    if x_label is None:
#        x_label = x
#    x_values = list(set(filter(lambda x: x is not None, properties.keys())))
#    x_values.sort()
#    y_values = [properties[x] for x in x_values]
#
#    plt.figure(figsize=(16, 9), dpi=80)
#    plt.plot(x_values, y_values)
#    plt.xscale(xscale)
#    # plt.ylim([-5, 105])
#    # plt.legend()
#    plt.xlabel(x_label)
#    plt.ylabel(y_label)
#    render(title, interactive, image_path)
#


def plot_apk_size(
    apk_data: list[Any],
    interactive: bool = True,
    image_path: Path | None = None,
):
    sizes = np.array([e["total_dex_size"] for e in apk_data]) / 1024 / 1024
    sizes.sort()
    plt.figure(figsize=(16, 9), dpi=80)
    plt.bar(np.arange(len(sizes)), sizes)
    plt.ylabel("Bytecode size (MiB)")
    plt.tick_params(
        axis="x",
        which="both",
        bottom=False,
        top=False,
        labelbottom=False,
    )
    for s in range(7, 13):
        plt.axhline(y=(4**s) / 1024 / 1024, color="r", linestyle=":")
    render("Bytecode size of the apks", interactive, image_path)


def plot_apk_size_hl_subset(
    apk_data: list[Any],
    subset_sha: list[str],
    title: str,
    interactive: bool = True,
    image_path: Path | None = None,
):
    apk_data.sort(key=lambda x: x["total_dex_size"])
    sizes = (
        np.array(
            [
                e["total_dex_size"] if e["sha256"] not in subset_sha else 0
                for e in apk_data
            ]
        )
        / 1024
        / 1024
    )
    sizes_hl = (
        np.array(
            [e["total_dex_size"] if e["sha256"] in subset_sha else 0 for e in apk_data]
        )
        / 1024
        / 1024
    )
    plt.figure(figsize=(16, 9), dpi=80)
    plt.bar(np.arange(len(sizes)), sizes, edgecolor="black")
    plt.bar(
        np.arange(len(sizes)), sizes_hl, color="#D55E00", hatch="x", edgecolor="black"
    )
    plt.ylabel("Bytecode size (MiB)")
    plt.tick_params(
        axis="x",
        which="both",
        bottom=False,
        top=False,
        labelbottom=False,
    )
    for s in range(7, 13):
        plt.axhline(y=(4**s) / 1024 / 1024, color="r", linestyle=":")
    render(title, interactive, image_path)
