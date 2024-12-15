all: run

.PHONY: run
run:
	python3.13 src/password_manager.py

.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ *.pyc *.pyo *.log .pytest_cache
	rm -rf build dist *.egg-info
	rm -rf .mypy_cache .coverage htmlcov
	rm -rf docs/_build
