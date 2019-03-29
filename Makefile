default: clean check test package install

.PHONY: clean
clean:
	rm -rf dist
	rm -rf termlink.egg-info

.PHONY: lint
lint:
	pylint -f parseable termlink tests | tee pylint.out

.PHONY: test
test:
	ENV=TEST nosetests --verbose -w tests

.PHONY: package
package:
	python setup.py sdist

.PHONY: install
install:
	python setup.py install