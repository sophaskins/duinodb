import library

boards = library.load_boards()
socs = library.load_socs()
chip_families = library.load_chip_families()
manufacturers = library.load_manufacturers()
flattened_socs = library.load_flattened_socs()
flattened_boards = library.load_flattened_boards()
pinouts = library.load_pinouts()

def validate_references(referrers, referents, field):
    for _, referrer in referrers.items():
        if referrer[field] not in referents:
            print("{} {} refers to non-existent {}: {}".format(referrer["kind"], referrer["id"], field, referrer[field]))

def validate_board_soc(board, flattened_socs):
    if "variations" in board:
        for variation in board["variations"]:
            if "soc" in variation:
                soc = variation["soc"]
            else:
                soc = board["common"]["soc"]

            if soc not in flattened_socs:
                print("invalid soc ({}) for board {} variation {}".format(soc, board["id"], variation["id"]))
    else:
        soc = board["common"]["soc"]
        if soc not in flattened_socs:
                print("invalid soc ({}) for board {}".format(soc, board["id"]))

def validate_board_manufacturers(board, manufacturers):
    if board["manufacturer"] not in manufacturers:
        print("invalid manufacturer {} for board {}".format(board["manufacturer"], board["id"]))

for _, board in boards.items():
    validate_board_soc(board, flattened_socs)
    validate_board_manufacturers(board, manufacturers)

validate_references(flattened_boards, pinouts, "pinout")
