"""Module for testing OneLevelOfIndentation Check"""
import astroid
import pylint.testutils
from object_calisthenics.checkers.one_level_of_indentation import OneLevelOfIndentation


class TestOneLevelOfIndentation(pylint.testutils.CheckerTestCase):
    """Test case for OneLevelOfIndentation checker."""
    CHECKER_CLASS = OneLevelOfIndentation

    def test_finds_two_levels_of_indentation_in_if(self):
        """Test should fail when there are two nested if statements."""
        func_node = astroid.extract_node("""
        def test():  #@
            hello = None
            if x > 10:
                if y > 5:
                    hello = 'world'
            return hello
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_finds_three_levels_of_indentation_in_if(self):
        """Test should fail when there are three nested if statements"""
        func_node = astroid.extract_node("""
                def test():  #@
                    hello = None
                    if x > 10:
                        if y > 5:
                            if z > 5:
                                hello = 'world'
                    return hello
                """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_finds_two_levels_of_indentation_in_for_loop(self):
        """Test should fail on two nested for loops"""
        func_node = astroid.extract_node("""
                        def test():  #@
                            hello = None
                            for i in range(3):
                                for j in range(3):
                                    hello = "world"
                        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_finds_two_levels_of_indentation_in_while_loop(self):
        """Test should fail in a function with a while loop and an extra nesting"""
        func_node = astroid.extract_node("""
                                def test():  #@
                                    while True:
                                        if a > 0:
                                            i = i + 1
                                """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_ok_with_single_indentation(self):
        """Test should pass when there is a single indentation in a function"""
        func_node = astroid.extract_node("""
                                def test():  #@
                                    hello = 'world'
                                    return hello
                                """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_finds_two_levels_of_indentation_in_second_block(self):
        """Test should fail when there are two nested statements anywhere in the function"""
        func_node = astroid.extract_node("""
                def test():  #@
                    hello = None
                    if x < 5:
                        hello = 'hello'
                    if x > 10:
                        if y > 5:
                            hello = 'world'
                    return hello
                """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_finds_two_indentations_in_nested_functions(self):
        """Test should fail if there is a nested function and a nested statement inside"""
        func_node = astroid.extract_node("""
                        def test():  #@
                            hello = 'world'
                            def test1():
                                some = 'thing'
                                if hello == 'world':
                                    hello = 'bye'
                            test1()
                        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0001",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_empty_function(self):
        """Test should pass in en empty function."""
        func_node = astroid.extract_node("""
                        def test():  #@
                            pass
                        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_multiple_single_indent_blocks(self):
        """Test should pass when function contains multiple one level indents"""
        func_node = astroid.extract_node("""
                        def test():  #@
                            if x > y:
                                y = x
                            if y > x:
                                x = y
                        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)
