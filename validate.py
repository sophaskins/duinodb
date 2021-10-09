import library

boards = library.load_boards()
socs = library.load_socs()
chip_families = library.load_chip_families()
manufacturers = library.load_manufacturers()
flattened_socs = library.load_flattened_socs()
flattened_boards = library.load_flattened_boards()
pinouts = library.load_pinouts()
headers = library.load_headers()

def validate_references(referrers, referents, field):
    referent_kind = next(iter(referents.values()))["kind"]
    for _, referrer in referrers.items():
        if referrer[field] not in referents:
            print("{} {} refers to non-existent {}: {}".format(referrer["kind"], referrer["id"], referent_kind, referrer[field]))

validate_references(flattened_boards, pinouts, "pinout")
validate_references(flattened_boards, flattened_socs, "soc")
validate_references(flattened_boards, manufacturers, "manufacturer")
validate_references(flattened_socs, chip_families, "chipFamily")
validate_references(flattened_boards, headers, "headers")
