"""Tests module for one dot per line check"""
import astroid
import pylint.testutils

from object_calisthenics.checkers.one_dot_per_line import OneDotPerLine


class TestOneDotPerLine(pylint.testutils.CheckerTestCase):
    # pylint: disable=W0006
    """Test case for OneDotPerLine checker."""
    CHECKER_CLASS = OneDotPerLine

    def test_check_fails_when_more_than_one_dot_per_line_in_assignment(self):
        """
        Check should fail when more than a single dot during assignment
        """
        call_node = astroid.extract_node("""
        def test_func():
            hello = obj1.obj2.func3() #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=call_node.value,
                    line=3,
                    col_offset=12,
                    end_line=3,
                    end_col_offset=29
                )
        ):
            self.checker.visit_call(call_node.value)

    def test_check_pass_when_one_dot_per_line_in_assignment(self):
        """
        Check should pass when a single dot during assignment
        """
        call_node = astroid.extract_node("""
                def test_func():
                    hello = obj1.func2() #@
                """)
        with self.assertNoMessages():
            self.checker.visit_call(call_node.value)

    def test_check_fails_when_more_than_one_dot_per_line_in_return(self):
        """
        Check should fail when more than a single dot call during return
        """
        call_node = astroid.extract_node("""
        def test_func():
            return obj1.obj2.func3()  #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=call_node.value,
                    line=3,
                    col_offset=11,
                    end_line=3,
                    end_col_offset=28
                )
        ):
            self.checker.visit_call(call_node.value)

    def test_check_pass_when_one_dot_per_line_in_return(self):
        """
        Check should pass when a single dot during return
        """
        call_node = astroid.extract_node("""
                def test_func():
                    return obj1.func2()  #@
                """)
        with self.assertNoMessages():
            self.checker.visit_call(call_node.value)

    def test_check_fails_when_more_than_one_dot_per_line_in_standalone_call(self):
        """
        Check should fail when more than a single dot call during standalone expression
        """
        call_node = astroid.extract_node("""
        def test_func():
            obj1.obj2.func3()  #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=call_node,
                    line=3,
                    col_offset=4,
                    end_line=3,
                    end_col_offset=21
                )
        ):
            self.checker.visit_call(call_node)

    def test_check_pass_when_only_one_dot_per_line_in_standalone_call(self):
        """
        Check should pass when a single dot during standalone
        """
        call_node = astroid.extract_node("""
                def test_func():
                    obj1.func2()  #@
                """)
        with self.assertNoMessages():
            self.checker.visit_call(call_node)

    def test_check_fails_when_more_than_one_dot_per_line_in_standalone_attribute(self):
        """
        Check should fail when more than a single dot attribute reference during
        standalone expression
        """
        attribute_node = astroid.extract_node("""
        def test_func():
            obj1.obj2.attr3  #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=attribute_node,
                    line=3,
                    col_offset=4,
                    end_line=3,
                    end_col_offset=21
                )
        ):
            self.checker.visit_attribute(attribute_node)

    def test_check_pass_when_one_dot_per_line_in_standalone_attribute(self):
        """
        Check should pass when a single dot during standalone
        """
        attribute_node = astroid.extract_node("""
        def test_func():
            obj1.attr2  #@
        """)
        with self.assertNoMessages():
            self.checker.visit_attribute(attribute_node)

    def test_check_fails_when_more_than_one_dot_per_line_in_assignment_attribute(self):
        """
        Check should fail when more than a single dot attribute reference during assignment
        """
        call_node = astroid.extract_node("""
        def test_func():
            hello = obj1.obj2.attr3 #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=call_node.value,
                    line=3,
                    col_offset=12,
                    end_line=3,
                    end_col_offset=29
                )
        ):
            self.checker.visit_attribute(call_node.value)

    def test_check_pass_when_one_dot_per_line_in_assignment_attribute(self):
        """
        Check should pass when a single dot during assignment
        """
        call_node = astroid.extract_node("""
                def test_func():
                    hello = obj1.attr2 #@
                """)
        with self.assertNoMessages():
            self.checker.visit_attribute(call_node.value)

    def test_check_pass_when_more_than_one_dot_per_line_in_return_attribute(self):
        """
        Check should fail when more than a single dot attribute reference during return
        """
        call_node = astroid.extract_node("""
        def test_func():
            return obj1.obj2.attr3  #@
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0006",
                    node=call_node.value,
                    line=3,
                    col_offset=11,
                    end_line=3,
                    end_col_offset=28
                )
        ):
            self.checker.visit_attribute(call_node.value)

    def test_check_pass_when_one_dot_per_line_in_return_attribute(self):
        """
        Check should pass when a single dot during return
        """
        call_node = astroid.extract_node("""
                def test_func():
                    return obj1.attr2  #@
                """)
        with self.assertNoMessages():
            self.checker.visit_attribute(call_node.value)
