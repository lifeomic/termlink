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
# uncomment the following line to enforce test coverage standards
# COVER_MIN_PERCENTAGE=100
COVER=--with-coverage \
	--cover-package=termlink \
	--cover-erase \
	--cover-tests \
	--cover-min-percentage=${COVER_MIN_PERCENTAGE} \
	--cover-branches \
	--cover-html
test:
	ENV=TEST nosetests ${COVER} -w tests

.PHONY: package
package:
	python setup.py sdist bdist_wheel

.PHONY: deploy
deploy:
	python -m twine upload dist/*
