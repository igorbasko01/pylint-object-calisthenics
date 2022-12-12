"""Small Class Size checker"""
from typing import TYPE_CHECKING, Optional
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class SmallClassSize(BaseChecker):
    """
    A class for checking that a class doesn't exceed a predefined
    number of lines.
    """

    name = "small-class-size"
    msgs = {
        "W9007": (
            "A class exceeds the amount of allowed lines.",
            "class-too-large",
            "The class has too many lines. Current lines: %s, max allowed: %s"
        )
    }

    options = (
        (
            "max-class-lines", {
                "default": 150,
                "type": "int",
                "help": "Max allowed lines in class",
            },
        ),
    )

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    def leave_classdef(self, node: nodes.ClassDef):
        """
        Check that the amount of lines in the class doesn't exceed max
        allowed lines.
        """
        max_lines_in_class = node.end_lineno
        max_allowed_lines = self.linter.config.max_class_lines  # pylint: disable=chain-of-method-calls
        if max_lines_in_class > max_allowed_lines:
            self.add_message("W9007", node=node, args=(max_lines_in_class, max_allowed_lines))
