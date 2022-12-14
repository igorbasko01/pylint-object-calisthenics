"""The object calisthenics pylint checkers"""
from typing import TYPE_CHECKING

from object_calisthenics.checkers.else_keyword_present import ElseKeywordPresent
from object_calisthenics.checkers.first_class_collections import FirstClassCollections
from object_calisthenics.checkers.one_dot_per_line import OneDotPerLine
from object_calisthenics.checkers.one_level_of_indentation import OneLevelOfIndentation
from object_calisthenics.checkers.primitive_obsession import PrimitiveObsession
from object_calisthenics.checkers.small_class_size import SmallClassSize

if TYPE_CHECKING:
    from pylint.lint import PyLinter


def register(linter: "PyLinter"):
    """This required method auto registers the checkers during initialization.
    :param linter: The linter to register the checker to.
    """
    linter.register_checker(OneLevelOfIndentation(linter))
    linter.register_checker(ElseKeywordPresent(linter))
    linter.register_checker(PrimitiveObsession(linter))
    linter.register_checker(FirstClassCollections(linter))
    linter.register_checker(OneDotPerLine(linter))
    linter.register_checker(SmallClassSize(linter))
