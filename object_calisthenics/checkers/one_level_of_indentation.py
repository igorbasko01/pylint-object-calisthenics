"""One level of indentation checker"""
from typing import TYPE_CHECKING, Optional
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter"):
    """This required method auto registers the checker during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(OneLevelOfIndentation(linter))


class OneLevelOfIndentation(BaseChecker):
    """A class for checking that functions have a single level of indentation."""

    name = "one-level-indentation"
    msgs = {
        "W0001": {
            "A function has more than one level of indentation.",
            "too-much-indentation",
            "A function should contain at most a single indentation."
        }
    }

    max_indentation_levels_allowed = 1

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    def _iterate_statements(self, node, indentations: int, max_indentations: int):
        for statement in node:
            max_indentations = self._check_indentation(statement, indentations, max_indentations)
        return max_indentations

    def _check_indentation(self, current_node, indentations: int, max_indentations: int = 0):
        if max_indentations > self.max_indentation_levels_allowed:
            return max_indentations
        if isinstance(current_node, list):
            max_indentations = self._iterate_statements(current_node,
                                                        indentations,
                                                        max_indentations)
        if hasattr(current_node, "body"):
            indentations += 1
            max_indentations = max(max_indentations, indentations)
            max_indentations = self._check_indentation(current_node.body,
                                                       indentations,
                                                       max_indentations)
            indentations -= 1
        return max_indentations

    def visit_functiondef(self, node: nodes.FunctionDef):
        """When visiting a function, check if more than one indentation present."""
        max_indentations = self._check_indentation(node.body, indentations=0)
        if max_indentations > self.max_indentation_levels_allowed:
            self.add_message("W0001", node=node)
