import requests
import logging
import shutil
import hashlib
import json
from utils import sha256_sum
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from androguard.core.bytecodes import apk as androguard_apk  # type: ignore

APK_INFO_FOLDER = Path(__file__).parent / "apk_info"
if not APK_INFO_FOLDER.exists():
    APK_INFO_FOLDER.mkdir()


class ApkRef:
    """The reference to an apk. The apk it referes to can be in the androzoo repository or
    on the local file system.
     - If the app is in androzoon the app is refered to by its sha256
     - If the app is on the local file system, the app is refered to by its path
    """

    RefType = Enum("RefType", ["ANDROZOO", "LOCAL"])

    def __init__(
        self,
        type_: "ApkRef.RefType",
        sha256: Optional[str] = None,
        path: Optional[Path] = None,
    ):
        self.type = type_
        self.sha256 = sha256
        if self.sha256 is not None:
            self.sha256 = self.sha256.strip().upper()
        self.path = path
        self.integrity_check()

    def __str__(self):
        return f"APK<{str(self.type)}: sha256={self.sha256}, path={str(self.path)}>"

    def integrity_check(self):
        """Check if the ApkRef is coherent."""
        if self.type == ApkRef.RefType.ANDROZOO and self.sha256 is None:
            raise RuntimeError(f"Androzoo ApkRef must have a sha256: {str(self)}")
        if self.type == ApkRef.RefType.LOCAL and self.path is None:
            raise RuntimeError(f"Local APkRef must have a path: {str(self)}")

    def get_path(self) -> Path:
        """Return the path to the apk."""
        if self.path is None:
            raise RuntimeError(f"{str(self)} don't have a path")
        return self.path

    def get_sha256(self) -> str:
        """Return the sha256 of the apk."""
        if self.sha256 is None:
            if self.path is None:
                raise RuntimeError(f"Could not compute hash for {str(self)}")
            self.sha256 = sha256_sum(self.path).upper()
        return self.sha256


def get_apk(apk_ref: ApkRef, path: Path, api_key: bytes):
    """Retrieve and apk from its reference and put it at `path`.
    `api_key` is always ask because it's easier that way."""
    if apk_ref.type == ApkRef.RefType.ANDROZOO:
        downlaod_apk(apk_ref.get_sha256(), api_key, path)
    elif apk_ref.type == ApkRef.RefType.LOCAL:
        shutil.copy(apk_ref.get_path(), path)


def downlaod_apk(apk_sha256: str, api_key: bytes, path: Path):
    """Download an apk from androzoo and store it at the given location"""
    logging.debug(f"Start downloading apk {apk_sha256}")
    resp = requests.get(
        "https://androzoo.uni.lu/api/download",
        params={
            b"apikey": api_key,
            b"sha256": apk_sha256.encode("utf-8"),
        },
    )
    with path.open("bw") as file:
        file.write(resp.content)
    logging.debug(f"Finished downloading apk {apk_sha256}")


def get_apk_info(apk_ref: ApkRef, api_key: bytes) -> dict[str, Any]:
    """Return the information availables about an application"""
    apk_path = APK_INFO_FOLDER / (apk_ref.get_sha256() + ".json")
    get_apk(apk_ref, apk_path, api_key)
    info: dict[str, Any] = {}
    info["apk_size"] = apk_path.stat().st_size
    info["sha256"] = apk_ref.get_sha256()
    if apk_ref.path is not None:
        info["file"] = apk_ref.path.name
    else:
        info["file"] = None

    try:
        apk = androguard_apk.APK(apk_path)
        info["name"] = apk.get_app_name()  # redundant with pkg_name ?
        info["min_sdk"] = apk.get_min_sdk_version()
        if info["min_sdk"] is not None:
            info["min_sdk"] = int(info["min_sdk"])
        info["max_sdk"] = apk.get_max_sdk_version()
        if info["max_sdk"] is not None:
            info["max_sdk"] = int(info["max_sdk"])
        info["target_sdk"] = apk.get_target_sdk_version()
        if info["target_sdk"] is not None:
            info["target_sdk"] = int(info["target_sdk"])
        info["total_dex_size"] = sum(
            map(lambda x: len(x), apk.get_all_dex())
        )  # TODO: faster to open the zip and use st_size?
    except:
        info["name"] = ""
        info["min_sdk"] = None
        info["max_sdk"] = None
        info["target_sdk"] = None
        info["total_dex_size"] = None
    apk_path.unlink()
    return info


def load_apk_info(apks: list[ApkRef], androzoo_list: Path, api_key: bytes):
    """Load the information for the provided apks (`apks` must contain the sha256 of the apk to load)
    from the androzoo_list. The information are then stored in json files"""
    logging.debug("Start extracting data from the androzoo list")
    apks_dict = {a.get_sha256().strip().upper(): a for a in apks}
    for apk in apks:
        apk_info_path = APK_INFO_FOLDER / (apk.get_sha256() + ".json")
        if apk_info_path.exists():
            del apks_dict[apk.get_sha256()]

    with androzoo_list.open("r") as list_file:
        first_line = list_file.readline()
        entrie_names = list(map(lambda x: x.strip(), first_line.split(",")))
        sha256_index = entrie_names.index(
            "sha256"
        )  # TODO: if 'sha256' is not found in the first line, we have the wrong file...
        while line := list_file.readline():
            if not apks_dict:
                break
            entries = list(map(lambda x: x.strip(), line.split(",")))
            # TODO: don't parse the entries manually...
            if len(entries) != len(entrie_names):
                entries_set = set(map(lambda x: x.upper(), entries))
                inter = entries_set.intersection(apks_dict.keys())
                if inter:
                    logging.warning(
                        f"The information for the apk {inter} may not be retreived from the list due to malformated line: {line}"
                    )
                    continue
            info: dict[str, Any] = {}
            sha256 = entries[sha256_index].upper()
            if sha256 in apks_dict:
                for (k, v) in zip(entrie_names, entries):
                    info[k] = v
                if "markets" in info:
                    info["markets"] = list(
                        map(lambda x: x.strip(), info["markets"].split("|"))
                    )
                if "apk_size" in info:
                    info["apk_size"] = int(info["apk_size"])
                if "vt_detection" in info:
                    info["vt_detection"] = int(info["vt_detection"])
                if "dex_size" in info:
                    info["dex_size"] = int(info["dex_size"])
                if "pkg_name" in info:
                    info["pkg_name"] = (
                        info["pkg_name"].removeprefix('"').removesuffix('"')
                    )
                apk_info_path = APK_INFO_FOLDER / (sha256 + ".json")
                info |= get_apk_info(apks_dict[sha256], api_key)
                with apk_info_path.open("w") as file:
                    json.dump(info, file)
                del apks_dict[sha256]
    for apk_hash in apks_dict:
        logging.warning(
            f"The information for the apk {apk_hash} was not found in the androzoo list"
        )
        info = get_apk_info(apks_dict[apk_hash], api_key)
        for key in entrie_names:
            if key not in info:
                info[key] = None
        apk_info_path = APK_INFO_FOLDER / (apk_hash + ".json")
        info |= get_apk_info(apks_dict[apk_hash], api_key)
        with apk_info_path.open("w") as file:
            json.dump(info, file)

    logging.debug(
        "Finished extracting the information about the apks from androzoo list"
    )
