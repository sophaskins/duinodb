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

def load_flattened_socs():
    socs = load_socs()
    flattened = {}
    for _, s in socs.items():
        base = s.copy()
        common = {}
        if "common" in s:
            common = s["common"].copy()
            del base["common"]

        if "variations" in s:
            del base["variations"]
            for v in s["variations"]:
                flattened[v["identifier"]] = (base | common) | v
        else:
            flattened[s["identifier"]] = base | common

    return flattened