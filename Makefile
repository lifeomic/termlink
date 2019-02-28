default: clean package

.PHONY: clean
clean:
	rm -rf dist
	rm -rf termlink.egg-info

.PHONY: test
test:
	ENV=test python -m unittest discover -s tests -p "*_test.py"

.PHONY: package
package:
	python setup.py sdist

.PHONY: install
install:
	python setup.py install