"""First Class Collections checker"""
from typing import TYPE_CHECKING, Optional, List

from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class FirstClassCollections(BaseChecker):
    """
    A class for checking that a class will contain only a single
    instance variable if it is of a collection type
    """

    name = "first-class-collections"
    msgs = {
        "W0004": {
            "A class contains more than a single instance variable when a collection is present",
            "single-collection-instance-variable",
            "A class shouldn't have more than a single instance variable when there is a "
            "collection instance variable."
        },
        "W0005": {
            ""
        }
    }

    collection_types = {'List', 'Dict', 'Set'}

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    def _is_collection(self, instance_variable: nodes.AssignAttr):
        parent = instance_variable.parent
        if isinstance(parent, nodes.AnnAssign):
            return parent.annotation.value.name in self.collection_types
        return False

    def leave_classdef(self, node: nodes.ClassDef):
        found_collection = any(self._is_collection(instance_variable[0])
                               for instance_variable
                               in node.instance_attrs.values())
        if found_collection and len(node.instance_attrs) > 1:
            self.add_message("W0004", node=node)