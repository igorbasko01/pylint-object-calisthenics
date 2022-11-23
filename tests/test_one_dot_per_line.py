import astroid
import pylint.testutils

from object_calisthenics.checkers.one_dot_per_line import OneDotPerLine


class TestOneDotPerLine(pylint.testutils.CheckerTestCase):
    """Test case for FirstClassCollections checker."""
    CHECKER_CLASS = OneDotPerLine

    def test_check_fails_when_more_than_one_dot_per_line_in_assignment(self):
        """
        """
        assn_node = astroid.extract_node("""
        def test_func():
            hello = obj1.obj2.func3() #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=assn_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_assign(assn_node)

    def test_check_fails_when_more_than_one_dot_per_line_in_return(self):
        """
        """
        func_node = astroid.extract_node("""
        def test_func():
            return obj1.obj2.func3()
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(func_node)

    def test_check_fails_when_more_than_one_dot_per_line_in_standalone_call(self):
        """
        """
        func_node = astroid.extract_node("""
        def test_func():
            obj1.obj2.func3()
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(func_node)