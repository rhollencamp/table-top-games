.PHONY: run test lint venv

run:
	PORT=8080 python3 -m ttg

test:
	python3 -m unittest

lint:
	pycodestyle ttg/*.py tests/*.py
	pylint ttg/*.py tests/*.py
