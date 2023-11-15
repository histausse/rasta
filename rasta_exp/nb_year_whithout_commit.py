#!/usr/bin/env python3

# Dep: GitPython

import time
from typing import Any
from git import Repo
from pathlib import Path

import json

SOURCES = {
    "a3e": "https://github.com/tanzirul/a3e",
    "a5": "https://github.com/tvidas/a5",
    "adagio": "https://github.com/hgascon/adagio",
    "amandroid": "https://github.com/arguslab/Argus-SAF",
    "anadroid": "https://github.com/maggieddie/pushdownoo",
    "androguard": "https://github.com/androguard/androguard/",
    "apparecium": "https://github.com/askk/apparecium",
    "blueseal": "https://github.com/ub-rms/blueseal",
    "choi_et_al": "https://github.com/kwanghoon/JavaAnalysis",
    "didfail": "https://bitbucket.org/wklieber/didfail.git",
    "droidsafe": "https://github.com/MIT-PAC/droidsafe-src",
    "flowdroid": "https://github.com/secure-software-engineering/FlowDroid",
    "gator": None,  # "http://web.cse.ohio-state.edu/presto/software/gator/",
    "ic3": "https://github.com/siis/ic3",
    "iccta": "https://github.com/lilicoding/soot-infoflow-android-iccta.git",
    "lotrack": "https://github.com/MaxLillack/Lotrack",
    "mallodroid": "https://github.com/sfahl/mallodroid",
    "redexer": "https://github.com/plum-umd/redexer",
    "saaf": "https://github.com/SAAF-Developers/saaf",
    "thresher": "https://github.com/cuplv/thresher",
    "thresher": "https://github.com/cuplv/thresher",
    "wognsen_et_al": "https://bitbucket.org/erw/dalvik-bytecode-analysis-tool.git",
}


# git clone --filter=blob:none --no-checkout --single-branch --branch master git://some.repo.git .


def rm_tree(path: Path):
    """Delete a whole tree from the file system"""
    if path.is_file():
        path.unlink()
    else:
        for child in path.iterdir():
            rm_tree(child)
        path.rmdir()


def get_nb_y_wo_commit(name, src) -> dict[str, Any]:
    p = Path("/") / "tmp" / "git_compute_years_witout_commit"
    p.mkdir(exist_ok=True)
    repo_path = p / name
    repo = Repo.clone_from(
        src, repo_path, multi_options=["--filter=blob:none", "--no-checkout"]
    )
    for ref in repo.remote().refs:
        repo.git.fetch(
            "origin", "/".join(str(ref).split("/")[1:]), "--filter=blob:none"
        )
    years = set()
    for c in repo.iter_commits("--all"):
        years.add(time.gmtime(c.authored_date).tm_year)
    first_year = min(years)
    current_year = time.localtime().tm_year
    nb_y_wo_commit = 0
    for y in range(first_year, current_year + 1):
        if y not in years:
            nb_y_wo_commit += 1
    print(f"Year of the first commit: {first_year}")
    print(
        f"NB of years without commit from {first_year} to {current_year}: {nb_y_wo_commit}"
    )

    rm_tree(repo_path)
    return {
        "name": name,
        "src": src,
        "year_first_commit": first_year,
        "year_wo_commit": nb_y_wo_commit,
    }


if __name__ == "__main__":
    results = [
        {
            "name": "gator",
            "src": "http://web.cse.ohio-state.edu/presto/software/gator/",
            "year_first_commit": 2014,
            "year_wo_commit": 4,
        }
    ]
    for tool in SOURCES:
        src = SOURCES[tool]
        if src is None:
            print(f"{tool}: Not a git repo")
        else:
            print(f"{tool}:")
            results.append(get_nb_y_wo_commit(tool, src))
        print()

    print(json.dumps(results))  # TODO: write in a format good for latex
