# SUDOKU makefile
# WSC, 1-Jan-2025


help:
	@echo "make pydoc                   ... generate pydoc documentation for sudoku_np1 class"

.PHONY: pydoc

pydoc: sudoku_np1.py
	python3 -m pydoc -w sudoku_np1
	cp sudoku_np1.html doc/_static

clean:
	rm -r __pycache__
