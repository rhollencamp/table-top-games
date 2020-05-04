.PHONY: run test lint venv

run:
	PORT=8080 .venv/bin/python3 table_top.py

test:
	.venv/bin/python3 -m unittest discover -b

lint:
	.venv/bin/pycodestyle *.py
	.venv/bin/pylint *.py

venv:
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt
