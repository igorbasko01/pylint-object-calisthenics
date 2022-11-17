pylint-run:
	pylint --recursive=yes --ignore=venv,build --load-plugins=object_calisthenics.checkers.one_level_of_indentation ./