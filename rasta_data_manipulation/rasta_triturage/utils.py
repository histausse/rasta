"""
Utils.
"""

import matplotlib.pyplot as plt  # type: ignore
import numpy as np
from slugify import slugify  # type: ignore
from typing import Any, Callable, Optional
from pathlib import Path
import sqlite3

DENSE_DASH = (0, (5, 1))
DENSE_DOT = (0, (1, 3))

MARKERS = {
    "adagio": ".",
    "amandroid": "o",
    "anadroid": "X",
    "androguard": "+",
    "androguard_dad": "v",
    "apparecium": "d",
    "blueseal": "^",
    "dialdroid": "<",
    "didfail": ">",
    "droidsafe": r"$\circ$",
    "flowdroid": r"$\boxplus$",
    "gator": r"$\otimes$",
    "ic3": "1",
    "ic3_fork": "s",
    "iccta": "P",
    "mallodroid": r"$\divideontimes$",
    "perfchecker": "*",
    "redexer": "x",
    "saaf": "D",
    "wognsen_et_al": r"$\rtimes$",
}

COLORS = {
    "didfail": "#1f77b4",
    "adagio": "#ff7f0e",
    "iccta": "#2ca02c",
    "androguard": "#d62728",
    "gator": "#9467bd",
    "mallodroid": "#8c564b",
    "dialdroid": "#e377c2",
    "androguard_dad": "#7f7f7f",
    "wognsen_et_al": "#bcbd22",
    "perfchecker": "#17becf",
    "amandroid": "#1f77b4",
    "ic3": "#ff7f0e",
    "apparecium": "#2ca02c",
    "blueseal": "#d62728",
    "droidsafe": "#9467bd",
    "redexer": "#8c564b",
    "anadroid": "#e377c2",
    "saaf": "#7f7f7f",
    "ic3_fork": "#bcbd22",
    "flowdroid": "#17becf",
    "adagio": "#1f77b4",
    "androguard": "#ff7f0e",
    "mallodroid": "#2ca02c",
    "androguard_dad": "#d62728",
    "wognsen_et_al": "#9467bd",
    "amandroid": "#8c564b",
    "apparecium": "#e377c2",
    "redexer": "#7f7f7f",
}


def get_list_tools(db: Path) -> list[str]:
    """Get the list of tool found in the database."""
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        tools = cur.execute("SELECT DISTINCT tool_name FROM exec;")
    return [tool[0] for tool in tools]


def radar_chart(
    axes: list[str],
    values: list[list[Any]],
    labels: list[str],
    title: str,
    interactive: bool,
    image_path: Path | None,
):
    plt.rc("grid", linewidth=1, linestyle="-")
    plt.rc("xtick", labelsize=15)
    plt.rc("ytick", labelsize=15)
    angles = np.linspace(0, 2 * np.pi, len(axes), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))  # type: ignore
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    for label, vals in zip(labels, values):
        vals = vals + [vals[0]]
        ax.plot(angles, vals, label=label, marker=MARKERS.get(label, "."))
        ax.fill(angles, vals, alpha=0.25)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, axes)
    ax.set_ylim(bottom=0)
    ax.grid(True)
    ncol = min(5, len(labels))
    ax.legend(
        loc="lower left",
        bbox_to_anchor=(0.0, -0.2, ncol * 1.0 / 5, 0.102),
        ncol=ncol,
        mode="expand",
        borderaxespad=0.0,
        fancybox=True,
        shadow=True,
        fontsize="xx-small",
    )
    render(title, interactive, image_path)


def render(
    title: str, interactive: bool, image_path: Path | None, tight_layout: bool = True
):
    """Render the figure. If `interactive`, display if, if `image_path`, save it."""
    # plt.title(title)
    if tight_layout:
        plt.tight_layout()
    if image_path is not None:
        if not image_path.exists():
            image_path.mkdir(parents=True, exist_ok=True)
        plt.savefig(image_path / (slugify(title) + ".pdf"), format="pdf")
    if interactive:
        plt.show()
    plt.close()


def mean(field: str) -> Callable[[list[Any]], float]:
    def compute_mean(data: list[Any]) -> float:
        s = 0
        n = 0
        for e in data:
            n += 1
            s += e[field]
        return 0.0 if n == 0 else s / n

    return compute_mean


def median(field: str) -> Callable[[list[Any]], float]:
    def compute_median(data: list[Any]) -> float:
        l = [e[field] for e in data if e[field] is not None]
        l.sort()
        if not l:
            return 0.0
        return l[len(l) // 2]

    return compute_median


def plot_generic(
    data: list[list[tuple[Any, Any]]],
    meta: list[tuple[str, Any, Any, str]],
    x_label: str,
    y_label: str,
    title: str,
    ylim: Optional[tuple[int, int]] = None,
    interactive: bool = True,
    image_path: Path | None = None,
):
    """Plot a list of curve represented by list[(x, y)]. meta is the list of (label, linestyle)
    for each plot.
    """
    plt.figure(figsize=(16, 9), dpi=80)
    for i, plot in enumerate(data):
        label, linestyle, marker, color = meta[i]
        plot.sort(key=lambda p: p[0])
        x_values = np.array([x for (x, _) in plot])
        y_values = np.array([y for (_, y) in plot])
        plt.plot(
            x_values[~np.isnan(y_values)],
            y_values[~np.isnan(y_values)],
            label=label,
            marker=marker,
            color=color,
            linestyle=linestyle,
        )
    if ylim is not None:
        plt.ylim(ylim)
    plt.legend(loc="upper center", ncol=4, bbox_to_anchor=(0.5, -0.1))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    render(title, interactive, image_path)
