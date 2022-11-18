pylint-run:
	pylint --recursive=yes --ignore=venv,build --load-plugins=object_calisthenics.checkers ./

tests-run:
	pytest

all: pylint-run tests-run