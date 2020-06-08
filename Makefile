PY=.venv/bin/python3

.PHONY: run
run:
	PORT=8080 $(PY) -m ttg

.PHONY: debug
debug:
	TTG_LOG_LEVEL=DEBUG PORT=8080 $(PY) -m ttg

.PHONY: test
test:
	$(PY) -m unittest

.PHONY: lint
lint:
	$(PY) -m pycodestyle ttg/*.py tests/*.py
	$(PY) -m pylint -d C0114,C0116 ttg/*.py
	$(PY) -m pylint -d C0114,C0115,C0116 tests/*.py
