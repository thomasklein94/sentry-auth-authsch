.PHONY: clean develop install-tests lint compile publish test

develop:
	pip install "pip>=7"
	pip install -e .
	make install-tests

install-tests:
	@echo pip install .[tests]
	pip install .[tests]

lint:
	@echo "--> Linting python"
	flake8 src
	@echo ""

test:
	@echo "--> Running Python tests"
	py.test tests || exit 1
	@echo ""

compile:
	python setup.py sdist bdist_wheel

publish: compile
	python setup.py upload

clean:
	rm -rf *.egg-info src/*.egg-info
	rm -rf dist build
