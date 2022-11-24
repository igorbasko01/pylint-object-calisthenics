"""One dot per line checker"""
from typing import TYPE_CHECKING, Optional
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class OneDotPerLine(BaseChecker):
    """
    A class for checking that statements only use a single dot,
    and that there is no call chaining.
    """

    name = "one-dot-per-line"
    msgs = {
        "W0006": {
            "A statement has a chain of method calls.",
            "chain-of-method-calls",
            "A statement should at most have a single method call."
        }
    }

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    def _multiple_dots(self, node: nodes.Attribute):
        if hasattr(node, 'expr') and hasattr(node.expr, 'expr'):
            return True
        return False

    def _add_message(self, node: nodes.Attribute):
        self.add_message("W0006", node=node)

    def visit_call(self, node: nodes.Call):
        """Check dot per line when function call"""
        func = node.func
        if self._multiple_dots(func):
            self._add_message(node)

    def visit_attribute(self, node: nodes.Attribute):
        """Check dot per line when referencing attribute"""
        if self._multiple_dots(node):
            self._add_message(node)
