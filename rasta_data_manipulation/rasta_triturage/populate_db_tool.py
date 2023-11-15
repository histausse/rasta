import sqlite3
from pathlib import Path


TOOL_INFO = [
    {
        "tool_name": "adagio",
        "use_python": True,
        "use_androguard": True,
    },
    {
        "tool_name": "amandroid",
        "use_scala": True,
        "use_soot": False,
        "use_apktool": True,
    },
    {
        "tool_name": "anadroid",
        "use_python": True,
        "use_java": True,
        "use_scala": True,
        "use_soot": False,
        "use_apktool": True,
    },
    {
        "tool_name": "androguard",
        "use_python": True,
        "use_androguard": True,  # Duh
    },
    {
        "tool_name": "androguard_dad",
        "use_python": True,
        "use_androguard": True,
    },
    {
        "tool_name": "apparecium",
        "use_python": True,
        "use_androguard": True,
    },
    {
        "tool_name": "blueseal",
        "use_java": True,
        "use_soot": True,
        "use_apktool": True,
    },
    {
        "tool_name": "dialdroid",
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "didfail",
        "use_python": True,
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "droidsafe",
        "use_python": True,
        "use_java": True,
        "use_soot": True,
        "use_apktool": True,
    },
    {
        "tool_name": "flowdroid",
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "gator",
        "use_python": True,
        "use_java": True,
        "use_soot": True,
        "use_apktool": True,
    },
    {
        "tool_name": "ic3",
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "ic3_fork",
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "iccta",
        "use_java": True,
        "use_soot": True,
        "use_apktool": True,
    },
    {
        "tool_name": "mallodroid",
        "use_python": True,
        "use_androguard": True,
    },
    {
        "tool_name": "perfchecker",
        "use_java": True,
        "use_soot": True,
    },
    {
        "tool_name": "redexer",
        "use_ocaml": True,
        "use_ruby": True,
        "use_apktool": True,
    },
    {
        "tool_name": "saaf",
        "use_java": True,
        "use_soot": False,
        "use_apktool": True,
    },
    {
        "tool_name": "wognsen_et_al",
        "use_python": True,
        "use_prolog": True,
        "use_apktool": True,
    },
]

for line in TOOL_INFO:
    for col in [
        "use_python",
        "use_java",
        "use_scala",
        "use_ocaml",
        "use_ruby",
        "use_prolog",
        "use_soot",
        "use_androguard",
        "use_apktool",
    ]:
        if col not in line:
            line[col] = False


def create_tool_table(db: Path):
    """Create the db/table if it does not exist."""
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        if (
            cur.execute("SELECT name FROM sqlite_master WHERE name='tool';").fetchone()
            is None
        ):
            cur.execute(
                (
                    "CREATE TABLE tool ("
                    "    tool_name, use_python, use_java, use_scala,"
                    "    use_ocaml, use_ruby, use_prolog, use_soot, "
                    "    use_androguard, use_apktool"
                    ");"
                )
            )
            con.commit()


def populate_tool(
    db: Path,
):
    """Add to database the tool information"""
    create_tool_table(db)
    # DROP table if already exist? replace value?
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.executemany(
            (
                "INSERT INTO tool VALUES("
                "    :tool_name, :use_python, :use_java, :use_scala,"
                "    :use_ocaml, :use_ruby, :use_prolog, :use_soot, "
                "    :use_androguard, :use_apktool"
                ");"
            ),
            TOOL_INFO,
        )
        con.commit()
