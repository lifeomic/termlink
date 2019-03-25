default: clean check test package install

.PHONY: clean
clean:
	rm -rf dist
	rm -rf termlink.egg-info

.PHONY: check
check:
	pylint -f parseable termlink tests | tee pylint.out

.PHONY: test
test:
	ENV=test python -m unittest discover -s tests -p "*_test.py"

.PHONY: package
package:
	python setup.py sdist

.PHONY: install
install:
	python setup.py install