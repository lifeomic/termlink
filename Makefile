default: clean lint test package

.PHONY: clean
clean:
	rm -rf build
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
	python setup.py sdist bdist_wheel

.PHONY: deploy
deploy:
	python -m twine upload dist/*