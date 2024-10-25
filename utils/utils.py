import datetime
import json
import os


def str_between(string: (str, bytes), start: (str, bytes), end: (str, bytes), replace_to: (str, bytes) = None):
    end_idx = start_idx = string.find(start) + len(start)
    if isinstance(end, list):
        while end_idx < len(string) and string[end_idx] not in end:
            end_idx += 1
    else:
        end_idx = string.find(end)

    if replace_to is None:
        return string[start_idx: end_idx], start_idx, end_idx
    return string[:start_idx] + replace_to + string[end_idx:]


def read_config(filepath: str) -> dict:
    try:
        file = open(filepath, "r", encoding='utf-8')
        config = json.load(file)
        file.close()

        if "db_host" not in config:
            config["db_host"] = os.environ["DATABASE_HOST"]
        if "db_port" not in config:
            config["db_port"] = os.environ["DATABASE_PORT"]
        if "db_user" not in config:
            config["db_user"] = os.environ["DATABASE_USER"]
        if "db_db" not in config:
            config["db_db"] = os.environ["DATABASE_DB"]
        if "db_password" not in config:
            config["db_password"] = os.environ["DATABASE_PASSWORD"]

        if "admin_username" not in config:
            config["admin_username"] = os.environ["ADMIN_USERNAME"]

        return config
    except Exception as e:
        print("Can't open and serialize json:", filepath)
        print(e)
        exit()


def count_lines(filename, chunk_size=4096) -> int:
    with open(filename) as file:
        return sum(chunk.count('\n') for chunk in iter(lambda: file.read(chunk_size), ''))


def times_to_str(object):
    for key in object.keys():
        if type(object[key]) is datetime.time:
            object[key] = object[key].isoformat()
        if type(object[key]) is datetime.date:
            object[key] = object[key].isoformat()


def list_times_to_str(listWithTimedelta):
    for el in listWithTimedelta:
        times_to_str(el)
