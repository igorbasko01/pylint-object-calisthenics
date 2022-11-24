"""Tests module for first class collections check"""
import astroid
import pylint.testutils

from object_calisthenics.checkers.first_class_collections import FirstClassCollections


class TestFirstClassCollections(pylint.testutils.CheckerTestCase):
    # pylint: disable=W0006
    """Test case for FirstClassCollections checker."""
    CHECKER_CLASS = FirstClassCollections

    def test_fail_check_when_more_than_one_member_when_one_is_collection_type(self):
        """
        Test that first class collection check fails if two members exist
        and one of them is of type collection.
        """
        class_node = astroid.extract_node("""
        class TestClass:
            def __init__(self):
                self.test_collection: List[str] = []
                self.test_int: int = 0
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0004",
                    node=class_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(class_node)

    def test_fail_check_when_more_than_one_member_when_one_is_dict_type(self):
        """
        Test that first class collection check fails if two members exist
        and one of them is of type collection.
        """
        class_node = astroid.extract_node("""
        class TestClass:
            def __init__(self):
                self.test_collection: Dict[str, str] = {}
                self.test_int: int = 0
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0004",
                    node=class_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(class_node)

    def test_fail_check_when_more_than_one_member_when_one_is_set_type(self):
        """
        Test that first class collection check fails if two members exist
        and one of them is of type collection.
        """
        class_node = astroid.extract_node("""
        class TestClass:
            def __init__(self):
                self.test_collection: Set[str] = Set()
                self.test_int: int = 0
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0004",
                    node=class_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(class_node)

    def test_pass_check_all_instance_variables_are_not_collections(self):
        """The check should pass when all the instance variables are not collections"""
        class_node = astroid.extract_node("""
        class TestClass:
            def __init__(self):
                self.test_collection: str = 'hello'
                self.test_int: int = 0
        """)
        with self.assertNoMessages():
            self.checker.leave_classdef(class_node)

    def test_fail_check_if_not_all_instance_variables_are_annotated(self):
        """
        The check should fail when at least a single instance
        variable has no type hint. Use a separate message for that.
        """
        class_node = astroid.extract_node("""
                class TestClass:
                    def __init__(self):
                        self.test_str = 'str'
                        self.test_int: int = 0
                """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W0005",
                    node=class_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.leave_classdef(class_node)


    def test_pass_check_only_single_collection_instance_variable(self):
        """Test that the check passes when the only instance variable is a collection"""
        class_node = astroid.extract_node("""
                class TestClass:
                    def __init__(self):
                        self.test_collection: List[str] = []
                """)
        with self.assertNoMessages():
            self.checker.leave_classdef(class_node)
