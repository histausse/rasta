import sqlite3
import time
import gzip
import csv
import datetime
import requests
import getpass
import dateutil.parser

from androguard.core.bytecodes import apk as androguard_apk
from pathlib import Path


def int_or_none(str_: str) -> int | None:
    if str_:
        return int(str_)
    else:
        return None


def create_apk_table(db: Path):
    """Create the db/table if it does not exist."""
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        if (
            cur.execute("SELECT name FROM sqlite_master WHERE name='apk'").fetchone()
            is None
        ):
            cur.execute(
                (
                    "CREATE TABLE apk("
                    "    sha256, first_seen_year, apk_size,"
                    "    vt_detection, min_sdk, max_sdk,"
                    "    target_sdk, apk_size_decile, dex_date date,"
                    "    pkg_name, vercode, vt_scan_date date,"
                    "    dex_size, added date, markets, dex_size_decile, "
                    "    dex_size_decile_by_year"
                    ")"
                )
            )
            con.commit()


def get_sha_set(dataset: Path) -> set[str]:
    """Read a set of sha256 from a file."""
    apk_set = set()
    with dataset.open() as f:
        for line in f.readlines():
            apk_set.add(line.strip())
    return apk_set


def populate_from_year_and_sdk(db: Path, year_and_sdk: Path, apks: set[str]):
    """Add to the info from year_and_sdk.csv.gz to the database
    for the apks in `apks`.
    """
    apks_not_found = apks.copy()
    with gzip.open(year_and_sdk, "rt", newline="") as f:
        reader = csv.DictReader(f, quotechar='"')
        fieldnames = reader.fieldnames
        assert fieldnames is not None
        for row in reader:
            if row["sha256"] not in apks:
                continue
            value = {
                "sha256": row["sha256"],
                "first_seen_year": int_or_none(row["first_seen_year"]),
                "vt_detection": int_or_none(row["vt_detection"]),
                "min_sdk": int_or_none(row["min_sdk"]),
                "max_sdk": int_or_none(row["max_sdk"]),
                "target_sdk": int_or_none(row["target_sdk"]),
                "apk_size_decile": 0,  # Computed at dataset generation
                "dex_size_decile": 0,  # Computed by compute_dex_decile
            }
            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute(
                    (
                        "INSERT INTO apk ("
                        "    sha256, first_seen_year, vt_detection,"
                        "    min_sdk, max_sdk, target_sdk, apk_size_decile,"
                        "    dex_size_decile"
                        ") VALUES("
                        "    :sha256, :first_seen_year, :vt_detection,"
                        "    :min_sdk, :max_sdk, :target_sdk, :apk_size_decile,"
                        "    :dex_size_decile"
                        ");"
                    ),
                    value,
                )
                con.commit()
            apks_not_found.remove(row["sha256"])
    for apk in apks_not_found:
        value = {
            "sha256": apk,
            "first_seen_year": None,
            "vt_detection": None,
            "min_sdk": None,
            "max_sdk": None,
            "target_sdk": None,
            "apk_size_decile": 0,
            "dex_size_decile": 0,  # Computed by compute_dex_decile
        }
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                (
                    "INSERT INTO apk ("
                    "    sha256, first_seen_year, vt_detection,"
                    "    min_sdk, max_sdk, target_sdk, apk_size_decile,"
                    "    dex_size_decile"
                    ") VALUES("
                    "    :sha256, :first_seen_year, :vt_detection,"
                    "    :min_sdk, :max_sdk, :target_sdk, :apk_size_decile,"
                    "    :dex_size_decile"
                    ");"
                ),
                value,
            )
            con.commit()


def populate_from_latest_with_added_date(
    db: Path, latest_with_added_date: Path, apks: set[str]
):
    """Add to the info from latest_with-added-date.csv.gz to the database
    for the apks in `apks`.
    """
    with gzip.open(latest_with_added_date, "rt", newline="") as f:
        reader = csv.DictReader(f, quotechar='"')
        fieldnames = reader.fieldnames
        assert fieldnames is not None
        for row in reader:
            if row["sha256"] not in apks:
                continue
            value = {
                "sha256": row["sha256"],
                "apk_size": int_or_none(row["apk_size"]),
                "dex_date": datetime.datetime.fromisoformat(row["dex_date"])
                if row["dex_date"]
                else None,
                "pkg_name": row["pkg_name"],
                "vercode": int_or_none(row["vercode"]),
                "vt_scan_date": datetime.datetime.fromisoformat(row["vt_scan_date"])
                if row["vt_scan_date"]
                else None,
                "dex_size": int_or_none(
                    row["dex_size"]
                ),  # Not necessary the right value if multiple dex are used, see 'fix_dex_size()'
                "added": dateutil.parser.isoparse(row["added"])
                if row["added"]
                else None,
                "markets": row["markets"],
            }
            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute(
                    "UPDATE apk "
                    "SET apk_size = :apk_size,"
                    "    dex_date = :dex_date,"
                    "    pkg_name = :pkg_name,"
                    "    vercode = :vercode,"
                    "    vt_scan_date = :vt_scan_date,"
                    "    dex_size = :dex_size,"
                    "    added = :added,"
                    "    markets = :markets "
                    "WHERE"
                    "    sha256 = :sha256;",
                    value,
                )
                con.commit()


def download_apk(sha256: str, api_key: bytes) -> bytes:
    while True:
        resp = requests.get(
            "https://androzoo.uni.lu/api/download",
            params={
                b"apikey": api_key,
                b"sha256": sha256.encode("utf-8"),
            },
        )
        if resp.status_code == 200:
            return resp.content
        else:
            print(resp)
            print(resp.content)
            time.sleep(1)


def fix_dex_size(db: Path, apks: set[str], androzoo_key: bytes):
    """Download the apk from androzoo, compute the total size
    of all .dex file and update the database.
    """
    for sha256 in apks:
        apk = download_apk(sha256, androzoo_key)
        apk = androguard_apk.APK(apk, raw=True, skip_analysis=True)
        dex_size = sum(map(lambda x: len(x), apk.get_all_dex()))
        with sqlite3.connect(db) as con:
            cur = con.cursor()
            cur.execute(
                ("UPDATE apk " "SET dex_size = ? " "WHERE" "    sha256 = ?;"),
                (dex_size, sha256),
            )
            con.commit()


def populate_db_apk(
    db: Path,
    dataset: Path,
    year_and_sdk: Path,
    latest_with_added_date: Path,
    fix_dsize: bool,
):
    """Populate the database with the apk informations."""
    if fix_dsize:
        androzoo_key = (
            getpass.getpass(prompt="androzoo apikey: ").strip().encode("utf-8")
        )
    create_apk_table(db)
    apks = get_sha_set(dataset)
    populate_from_year_and_sdk(db, year_and_sdk, apks)
    populate_from_latest_with_added_date(db, latest_with_added_date, apks)
    if fix_dsize:
        fix_dex_size(db, apks, androzoo_key)
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE apk "
            "SET dex_size_decile = compute.decile "
            "FROM ("
            "    SELECT NTILE ( 10 ) OVER ( ORDER BY dex_size ) decile, sha256 FROM apk"
            ") AS compute "
            "WHERE apk.sha256 = compute.sha256;"
        )
        cur.execute(
            "UPDATE apk "
            "SET dex_size_decile_by_year = compute.decile "
            "FROM ("
            "    SELECT NTILE ( 10 ) "
            "    OVER ( PARTITION BY first_seen_year ORDER BY dex_size ) decile, sha256 "
            "    FROM apk"
            ") AS compute "
            "WHERE apk.sha256 = compute.sha256;"
        )
        con.commit()
