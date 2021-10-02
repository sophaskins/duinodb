generate:
	python3 make_boards.py

clean:
	find boards -name '*.yaml' -delete
	find manufacturers -name '*.yaml' -delete
	find chip-families -name '*.yaml' -delete
	find socs -name '*.yaml' -delete