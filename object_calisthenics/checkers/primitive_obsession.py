"""Primitive Obsession checker"""
from typing import TYPE_CHECKING, Optional, Union, Sequence
from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class PrimitiveObsession(BaseChecker):
    """A class for checking that functions have only typed arguments with custom types."""

    name = "primitive-obsession"
    msgs = {
        "W0003": {
            "A function argument can't be of a primitive type.",
            "dont-use-primitives",
            "A function argument should be of a custom type."
        }
    }

    primitives = ['str', 'int', 'float', 'bool', 'bytes', 'bytearray']

    def __init__(self, linter: Optional["PyLinter"] = None):
        super().__init__(linter)

    @staticmethod
    def _is_annotated(annotation: nodes.Name):
        if annotation:
            return True
        return False

    def _is_primitive(self, annotation: nodes.Name):
        is_annotated = self._is_annotated(annotation)
        if is_annotated and annotation.name in self.primitives:
            return True
        return False

    def _sequence_of_types_contains_primitive(self, types: Sequence[nodes.Name]):
        return any(self._contains_primitive(a_type) for a_type in types)

    def _contains_primitive(self, node: Union[nodes.Name, nodes.Subscript, nodes.Tuple]):
        if node is None or node == []:
            return True  # Un annotated args are considered primitives.
        if isinstance(node, nodes.Name):
            return self._is_primitive(node)
        if isinstance(node, nodes.Subscript):
            return self._contains_primitive(node.slice)
        if isinstance(node, nodes.Tuple):
            return self._sequence_of_types_contains_primitive(node.elts)
        return False

    @staticmethod
    def _clean_annotations(args: nodes.Arguments):
        if len(args.args) > 0 and args.args[0].name == 'self':
            return args.annotations[1:]
        return args.annotations

    def visit_functiondef(self, node: nodes.FunctionDef):
        """
        When visiting a function make sure that it only contains arguments with
        non-primitive types
        """
        annotations = self._clean_annotations(node.args)
        has_primitives = any(self._contains_primitive(annotation) for annotation in annotations)
        if has_primitives:
            self.add_message("W0003", node=node)
