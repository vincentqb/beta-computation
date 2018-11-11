notebook:
	jupyter-notebook src/Exploration.ipynb
report:
	jupyter-nbconvert src/Exploration.ipynb --to html --output-dir ./reports/
docs:
	pydoc3 src/* > docs/docs.txt
test:
	py.test-3 tests/Test.py
requirements:
	pip3 freeze > requirements.txt
