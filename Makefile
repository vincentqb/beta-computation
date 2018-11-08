notebook:
	jupyter-notebook src/Exploration.ipynb
report:
	jupyter-nbconvert src/Exploration.ipynb --to html --output-dir ./reports/
test:
	python3 src/Test.py
requirements:
	pip3 freeze > requirements.txt
