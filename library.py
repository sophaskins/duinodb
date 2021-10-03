import yaml
import glob

def load_items(kind):
    items = {}
    filenames = glob.glob("./{}/*.yaml".format(kind))
    for filename in filenames:
        with open (filename, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            items[data["identifier"]] = data
    return items

def load_boards():
    return load_items("boards")

def load_chip_families():
    return load_items("chip-families")

def load_manufacturers():
    return load_items("manufacturers")

def load_socs():
    return load_items("socs")

def load_flattened(kind):
    items = load_items(kind)
    flattened = {}
    for _, item in items.items():
        base = item.copy()
        common = {}
        if "common" in item:
            common = item["common"].copy()
            del base["common"]

        if "variations" in item:
            del base["variations"]
            for variation in item["variations"]:
                flattened[variation["identifier"]] = (base | common) | variation
        else:
            flattened[item["identifier"]] = base | common

    return flattened

def load_flattened_socs():
    load_flattened("socs")

def load_flattened_boards():
    load_flattened("boards")