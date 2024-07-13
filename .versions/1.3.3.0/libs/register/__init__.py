import yaml
import os
import hashlib


def register(path: str, database_path: str):
    if os.path.exists(database_path):
        mode = "r"
    else:
        mode = "w+"
    with open(database_path, mode, encoding="utf8") as file:
        data: dict = yaml.load(file, yaml.Loader)
    if data == None:
        data = dict()
    m = hashlib.md5(path.encode("utf8"))
    data["0x" + m.hexdigest()[:4].upper()] = path
    with open(database_path, 'w', encoding="utf8") as file:
        yaml.dump(data, file, encoding="uft8",
                  allow_unicode=True, sort_keys=False)


# register("12345678", r"F:\QuickProgram Files\WindowContentMenuEx(MYTOOL)\libs\register")
