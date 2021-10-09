import yaml
import glob
import os

def load_items(kind):
    items = {}
    filenames = glob.glob("./{}/*.yaml".format(kind))
    for filename in filenames:
        with open (filename, "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

            # filename (minus yaml) should match the id of the base resource
            # in order to help us naturally avoid id collisions
            filename_bit_that_should_match_id = os.path.basename(filename[:-5])
            if filename_bit_that_should_match_id != data["id"]:
                print("File {} contains a resource whose id is \"{}\", instead of the expected \"{}\"".format(filename, data["id"], filename_bit_that_should_match_id))

            items[data["id"]] = data
    return items

def load_boards():
    return load_items("boards")

def load_chip_families():
    return load_items("chip-families")

def load_manufacturers():
    return load_items("manufacturers")

def load_socs():
    return load_items("socs")

def load_pinouts():
    return load_items("pinouts")

def load_headers():
    return load_items("headers")

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
                prospective_id = variation["id"]
                if prospective_id in flattened:
                    print("WARNING: multiple objects/variations ({}) with id: {}".format(item["kind"], prospective_id))
                flattened[prospective_id] = (base | common) | variation
        else:
            prospective_id = item["id"]
            if prospective_id in flattened:
                print("WARNING: multiple objects/variations with id")
            flattened[prospective_id] = base | common

    return flattened

def load_flattened_socs():
    return load_flattened("socs")

def load_flattened_boards():
    return load_flattened("boards")
