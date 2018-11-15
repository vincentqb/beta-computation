.PHONY: notebook report docs test requirements

notebook:
	jupyter-notebook src/Exploration.ipynb
report:
	jupyter-nbconvert src/Exploration.ipynb --to html --output-dir ./reports/
docs:
	pydoc3 src/*.py > docs/docs.txt
test:
	py.test-3 tests/Test.py
requirements-freeze:
	pip3 freeze > requirements.txt
requirements-install:
	pip3 install -r requirements.txt
