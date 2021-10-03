import library

boards = library.load_boards()
socs = library.load_socs()
chip_families = library.load_chip_families()
manufacturers = library.load_manufacturers()
flattened_socs = library.load_flattened_socs()

def validate_board_soc(board, flattened_socs):
    if "variations" in board:
        for variation in board["variations"]:
            if "soc" in variation:
                soc = variation["soc"]
            else:
                soc = board["common"]["soc"]

            if soc not in flattened_socs:
                print("invalid soc ({}) for board {} variation {}".format(soc, board["identifier"], variation["identifier"]))
    else:
        soc = board["common"]["soc"]
        if soc not in flattened_socs:
                print("invalid soc ({}) for board {}".format(soc, board["identifier"]))

def validate_board_manufacturers(board, manufacturers):
    if board["manufacturer"] not in manufacturers:
        print("invalid manufacturer {} for board {}".format(board["manufacturer"], board["identifier"]))

for _, board in boards.items():
    validate_board_soc(board, flattened_socs)
    validate_board_manufacturers(board, manufacturers)