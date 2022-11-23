"""One dot per line checker"""
from typing import TYPE_CHECKING, Optional
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class OneDotPerLine(BaseChecker):
    """A class for checking that statements only use a single dot, and that there is no call chaining."""

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

    def visit_assign(self, node: nodes.Assign):
        pass
