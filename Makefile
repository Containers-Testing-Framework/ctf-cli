clean:
	@find . -name "*.pyc" -exec rm -rf {} \;

release: clean
	python setup.py clean
	python setup.py register
	python setup.py sdist
	python setup.py sdist upload
