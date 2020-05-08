PY=.venv/bin/python3

.PHONY: run
run:
	PORT=8080 $(PY) -m ttg

.PHONY: test
test:
	$(PY) -m unittest

.PHONY: lint
lint:
	$(PY) -m pycodestyle ttg/*.py tests/*.py
	$(PY) -m pylint -d C0116 ttg/*.py
	$(PY) -m pylint -d C0116,C0115,C0114 tests/*.py
