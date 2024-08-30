import pathlib
from pathlib import Path
import requests
import json
import os
import sys

from logging import getLogger, StreamHandler, INFO, Formatter

# ログの設定
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("[%(asctime)s] | %(message)s"))
logger = getLogger()
logger.addHandler(handler)
logger.setLevel(INFO)


def dlAllFiles(info_dir, save_dir):
    info_dir = pathlib.Path(info_dir)
    logger.debug(f"info_dir: {info_dir}")
    logger.info(f"Drive file information: {info_dir}")

    # ファイルの保存先
    logger.info(f"Saving files to       : {save_dir}")
    save_dir = pathlib.Path(save_dir)
    save_dir.mkdir(exist_ok=True)
    logger.debug(f"save_dir: {save_dir}")

    # ファイル一覧を取得
    files = info_dir.iterdir()

    info_list = []

    # ファイルをダウンロード
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
            for i in data:
                url = i["url"]
                name = i["name"]
                folderId = i["folderId"]
                info = {"url": url, "name": name, "folderId": folderId}
                info_list.append(info)

    for info in info_list:
        url = info["url"]
        name = info["name"]
        folderId = info["folderId"]

        if folderId != None:
            save_path = pathlib.Path(f"{save_dir}\\{folderId}")
            save_path.mkdir(exist_ok=True)
        else:
            save_path = pathlib.Path(f"{save_dir}")
            save_path.mkdir(exist_ok=True)

        logger.debug(f"save_path: {save_path}")

        filename = f"{save_path}\\{name}"
        if os.path.isfile(filename):
            tmp = Path(filename)
            filename = os.path.dirname(filename) + "\\" + tmp.stem + "_1" + tmp.suffix

        logger.info(f"Now Downloading: {filename}")

        r = requests.get(url, stream=True)

        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()


if __name__ == "__main__":
    args = sys.argv
    if 3 <= len(args):
        logger.debug(f"args: {args}")
        dlAllFiles(str(args[1]), str(args[2]))
    else:
        print(
            """
Usage: python dlAllFiles.py <info_dir> <save_dir>

info_dir: The directory where the file information is stored.
            Using "getAllFiles.py" to make the file information.
save_dir: The directory where the files are saved."""
        )
