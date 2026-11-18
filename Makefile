.PHONY: run test clean

PYTHON ?= python3

run:
	$(PYTHON) -m src.main config.csv

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -f *.png *.svg
