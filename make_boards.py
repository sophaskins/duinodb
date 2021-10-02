import csv
import yaml

def make_board_short_name(row):
    return "{}-{}".format(row["Manufacturer"], row["Model"]).lower().replace(" ", "-").replace("/", "-")

def make_board(row):
    variations = []
    if row["Link (presoldered headers)"]:
        variations.append({
            "price": float(row["Price"][1:].strip()),
            "link": row["Link (presoldered headers)"],
            "headers": "presoldered-pin",
        })
    if row["Link (no soldered headers)"]:
        variations.append({
            "price": float(row["Price2"][1:].strip()),
            "link": row["Link (no soldered headers)"],
            "headers": "unsoldered",
        })
    if row["Link (presoldered stacking headers)"]:
        variations.append({
            "price": float(row["Price "][1:].strip()),
            "link": row["Link (presoldered stacking headers)"],
            "headers": "presoldered-stacking",
        })

    data = {
        "kind": "Board",
        "name": row["Model"],
        "identifier": make_board_short_name(row),
        "manufacturer": row["Manufacturer"],
        "common": {
            "pinout": row["Pinout"],
            "soc":row["SoC"].lower().replace(" ", "-").replace(".", ""),
            "sram": row["SRAM"],
            "flash": row["Flash ROM"],
            "voltage": float(row["Voltage"]),
        },
    }

    if len(variations) > 1:
        data["variations"] = variations
    else:
        for k, v in variations[0].items():
            data["common"][k] = v

    if "external flash" in row and row["external flash"]:
        data["common"]["externalFlash"] = row["external flash"]
    if "psram" in row and row["psram"]:
        data["common"]["psram"] = row["psram"]
    return data

rows = []
with open("./excel.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

for r in rows:
    with open("./boards/{}.yaml".format(make_board_short_name(r)), "x") as f:
        data = make_board(r)
        yaml.dump(data, f, sort_keys=False)

for m in set([r["Manufacturer"] for r in rows]):
    short_name = m.lower().replace(" ", "-")
    data = {
        "kind": "Manufacturer",
        "name": m,
        "identifier": short_name,
    }
    with open("./manufacturers/{}.yaml".format(short_name), "x") as f:
        yaml.dump(data, f, sort_keys=False)

for cf in set([r["Chip Family"] for r in rows]):
    short_name = cf.lower().replace("+", "plus").replace(" ", "-")
    with open("./chip-families/{}.yaml".format(short_name), "x") as f:
        data = {
            "kind": "ChipFamily",
            "name": cf,
            "identifier": short_name,
        }
        yaml.dump(data, f, sort_keys=False)

for soc in set([(r["Chip Family"], r["SoC"]) for r in rows]):
    short_cf = soc[0].lower().replace("+", "plus").replace(" ", "-")
    short_soc = soc[1].lower().replace(" ", "-").replace(".", "")
    with open("./socs/{}.yaml".format(short_soc), "x") as f:
        data = {
            "kind": "SoC",
            "name": soc[1],
            "identifier": short_soc,
            "chipFamily": short_cf,
        }
        yaml.dump(data, f, sort_keys=False)

