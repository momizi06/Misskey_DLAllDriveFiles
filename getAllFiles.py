import sys
import os
from time import sleep
import requests
import json
from logging import getLogger, StreamHandler, INFO, Formatter

# ログの設定
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(Formatter("[%(asctime)s] | %(message)s"))
logger = getLogger()
logger.addHandler(handler)
logger.setLevel(INFO)


def misskey_api(endpoint: str, server: str, token: str, body: dict) -> None:
    url = f"{server}/api/{endpoint}"
    headers = {"Content-Type": "application/json"}
    data = {"i": token}
    if body:
        data.update(body)

    logger.debug(f"{data}")
    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        logger.error(response.json())
    else:
        logger.debug(f"Successfully called {endpoint}.")
        return response.json()


def getAllFiles(server, token, save_dir):
    logger.info(f"Creating {save_dir} directory...")
    os.makedirs(save_dir, exist_ok=True)

    logger.info("Getting your Drive files information...")
    logger.info("Now : No. 1 ~ 100")

    tmp_count = 0

    last_path = f"{save_dir}\\response1.json"
    response = misskey_api(
        "drive/stream", server, token, body={"limit": 100, "sort": "+createdAt"}
    )

    with open(last_path, "w") as f:
        f.write(json.dumps(response, indent=2))
    for i in range(2, 1000):
        tmpid = response[-1]["id"]
        logger.debug(f"tmpid: {tmpid}")
        sleep(1)
        response = misskey_api(
            "drive/stream",
            server,
            token,
            body={"limit": 100, "sort": "+createdAt", "untilId": tmpid},
        )
        if not response:
            break
        logger.info(f"Now : No. {(i - 1)*100 + 1} ~ {i*100}")
        tmp_count = i
        last_path = f"{save_dir}\\response{i}.json"
        with open(last_path, "w") as f:
            f.write(json.dumps(response, indent=2))

    logger.info("Successfully got Drive files information.")

    with open(last_path, "r") as f:
        data = json.load(f)
        logger.info(
            f"Make sure your Drive file count is {(tmp_count - 1) * 100 + len(data)}."
        )

    logger.info(
        f"If you unsure about the count, please check '{server}/settings/account-stats'."
    )


if __name__ == "__main__":
    args = sys.argv
    if 3 <= len(args):
        logger.debug(f"args: {args}")
        getAllFiles(str(args[1]), str(args[2]), str(args[3]))
    else:
        print(
            """
Usage     : python getAllFiles.py <server_url> <token> <save_dir>

server_url: The URL of the Misskey server.
            e.g. "https://misskey.io"
token     : The API token of the Misskey server.
            Token needs "Access your Drive files and folders" permission.
save_dir  : The directory where the files are saved."""
        )
