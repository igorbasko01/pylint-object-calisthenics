"""Tests module for the ElseKeywordPresent checker"""
import astroid
import pylint.testutils

from object_calisthenics.checkers.else_keyword_present import ElseKeywordPresent


class TestElseKeywordPresent(pylint.testutils.CheckerTestCase):
    # pylint: disable=W0006
    """Test case for ElseKeywordPresent checker."""
    CHECKER_CLASS = ElseKeywordPresent

    def test_else_present_in_function(self):
        """Test should fail when there is an else statement in a function"""
        func_node = astroid.extract_node("""
        def test():  #@
            hello = None
            if x > 10:
                hello = 'world'
            else:
                hello = 'universe'
            return hello
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0002",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_no_else_in_function(self):
        """Test should succeed when no else is found"""
        func_node = astroid.extract_node("""
        def test():  #@
            if x > 10:
                return 'world'
            return 'universe'
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)
