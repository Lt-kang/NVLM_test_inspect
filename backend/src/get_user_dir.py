from pathlib import Path
import json
import shutil
import os

import yaml

with open(Path(__file__).parent.parent / "config.yaml", "r") as f:
    config = yaml.safe_load(f)

user_dir_path = config["user_dir_path"]
user_mapping_path = config["user_mapping_path"]

user_mapping_dir = Path(user_mapping_path)
if not user_mapping_dir.exists():
    with open(user_mapping_dir, "w", encoding="utf-8") as f:
        json.dump({}, f)

with open(user_mapping_dir, "r", encoding="utf-8") as f:
    user_mapping = json.load(f)

    if user_mapping == "":
        user_mapping = {}

    user_list = list(user_mapping.keys())




def get_user_dir(user_id, init=False):
    if user_id in user_list:
        if init and Path(user_mapping[user_id]).exists():
            shutil.rmtree(user_mapping[user_id])
            os.makedirs(user_mapping[user_id], exist_ok=True)

    else:
        '''
        user_id가 user_list에 없을 경우
        '''
        user_mapping[user_id] = str(Path(user_dir_path) / str(user_id).split(".")[-1])
        with open(user_mapping_dir, "w", encoding="utf-8") as f:
            json.dump(user_mapping, f)

    user_dir = user_mapping[user_id]
    os.makedirs(user_dir, exist_ok=True)
    return Path(user_dir)
