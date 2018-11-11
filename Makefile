notebook:
	jupyter-notebook src/Exploration.ipynb
report:
	jupyter-nbconvert src/Exploration.ipynb --to html --output-dir ./reports/
test:
	py.test-3 src/Test.py
requirements:
	pip3 freeze > requirements.txt
docs:
	 pydoc3 src/* > docs/docs.txt
