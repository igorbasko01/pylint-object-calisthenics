"""Else Keyword Present checker"""
from typing import TYPE_CHECKING, Optional

from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class ElseKeywordPresent(BaseChecker):
    """A class for checking that functions don't use the else keyword."""

    name = "else-keyword-present"
    msgs = {
        "W9002": (
            "A function contains an else keyword",
            "dont-use-else",
            "A function shouldn't use an else keyword"
        )
    }

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    @staticmethod
    def _contains_else(node: nodes.If):
        if hasattr(node, "orelse") and node.orelse:
            return True
        return False

    def _iterate_statements(self, node: nodes.NodeNG):
        result = False
        for statement in node:
            is_else_found = self._check_indentation(statement)
            result = result | is_else_found
        return result

    def _check_indentation(self, current_node: nodes.NodeNG):
        is_else_found = False
        if isinstance(current_node, nodes.If):
            is_else_found = self._contains_else(current_node)
        if isinstance(current_node, list):
            is_else_found = self._iterate_statements(current_node)
        if hasattr(current_node, "body") and not is_else_found:
            is_else_found = self._check_indentation(current_node.body)
        return is_else_found

    def visit_functiondef(self, node: nodes.FunctionDef):
        """Check if an else keyword is present in the function"""
        is_else_found = self._check_indentation(node.body)
        if is_else_found:
            self.add_message("W9002", node=node)
