# Object Calisthenics Pylint Plugin

This is a Pylint Plugin that analyzes python code and evaluates if it
adheres to the Object Calisthenics rules that were coined by Jeff Bay.

## Execution
Currently, this plugin is not packaged, which means that cloning this project
is necessary to be able to use the plugin.

To use the plugin run: `pylint --recursive=yes --ignore=venv,build --load-plugins=object_calisthenics.checkers .`