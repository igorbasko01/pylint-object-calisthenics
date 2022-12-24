"""Module for checking that a Package contains a small amount of files"""
from typing import TYPE_CHECKING, Optional

from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PackageSize(BaseChecker):
    """A class for checking that the amount of files in package is small"""
    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)
