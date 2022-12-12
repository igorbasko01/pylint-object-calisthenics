"""Test module for small class size check"""
import astroid
import pylint.testutils

from object_calisthenics.checkers.small_class_size import SmallClassSize


class TestSmallClassSize(pylint.testutils.CheckerTestCase):
    # pylint: disable=W9006
    """Test case for SmallClassSize checker."""
    CHECKER_CLASS = SmallClassSize

    def test_class_is_large(self):
        """Check should fail if class has too many lines"""
        class_node = astroid.extract_node("""
        class TestClass:  #@
            def __init__(self):
                self.hello = 'hello'
                self.world = 'world'
                self.long = 'long'
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9007",
                    node=class_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=15,
                    args=(6, 3)
                )
        ):
            self.checker.linter.config.max_class_lines = 3
            self.checker.leave_classdef(class_node)

    def test_class_is_small(self):
        """The check should pass if the class is small."""
        class_node = astroid.extract_node("""
        class TestClass:  #@
            def __init__(self):
                self.hello = 'hello'
                self.world = 'world'
                self.long = 'long'
        """)
        with self.assertNoMessages():
            self.checker.leave_classdef(class_node)
