.PHONY: test pycodestyle venv run

run:
	.venv/bin/python3 table_top.py

test:
	.venv/bin/python3 -m unittest discover -b

lint:
	.venv/bin/pycodestyle --exclude=.venv --max-line-length=100 .

venv:
	python3 -m venv .venv
	.venv/bin/pip3 install -r requirements.txt
