"""Tests module for primitive obsession check"""
import astroid
import pylint.testutils

from object_calisthenics.checkers.primitive_obsession import PrimitiveObsession


class TestPrimitiveObsession(pylint.testutils.CheckerTestCase):
    # pylint: disable=chain-of-method-calls
    # pylint: disable=class-too-large
    """Test case for PrimitiveObsession checker."""
    CHECKER_CLASS = PrimitiveObsession

    def test_primitive_types_found_in_function_arguments(self):
        """Test that primitive arguments fail the check"""
        func_node = astroid.extract_node("""
        def test(hello: str, world: int):  #@
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_no_type_hints_in_function_arguments(self):
        """Test that arguments without type hints fail the check"""
        func_node = astroid.extract_node("""
        def test(hello, world):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_single_argument_has_no_type_hint(self):
        """Test that even a single argument without a type hint fails the check"""
        func_node = astroid.extract_node("""
        def test(hello: SomeType, world):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_sequence_types_with_primitives(self):
        """
        Test that an argument with a sequence type that contains primitive type
        fails the check.
        """
        func_node = astroid.extract_node("""
        def test(hello: List[str], world: SomeClassType):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_sequence_types_with_non_primitives(self):
        """
        Test that arguments with a sequence type that contains a non-primitive
        passes the check.
        """
        func_node = astroid.extract_node("""
        def test(hello: List[SomeClassType], world: SomeClassType):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_bytes_sequence_type(self):
        """Test that an argument with a bytes type fails the check"""
        func_node = astroid.extract_node("""
        def test(hello: bytes, world: SomeClassType):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_bytearray_sequence_type(self):
        """Test that a bytearray argument fails the check"""
        func_node = astroid.extract_node("""
        def test(hello: bytearray, world: SomeClassType):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_set_types_with_primitives(self):
        """
        Test that a set type argument that contains a primitive type
        is failing the check.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Set[str]):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_set_types_with_non_primitives(self):
        """
        Test that a set type argument with a non-primitive type
        passes the check.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Set[SomeClassType]):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_dict_type_with_primitive_key(self):
        """
        Test that a Dict type argument with a primitive type as the key
        fails the check.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Dict[str, SomeClassType]):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_dict_type_with_primitive_value(self):
        """
        Test that a Dict type argument with a primitive type as the value
        fails the check.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Dict[SomeClassType, str]):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_dict_type_with_no_primitives(self):
        """
        Test that a Dict type argument with a non-primitive type as the key and the value
        passes the check.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Dict[SomeKeyClass,SomeValueClass]):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_function_with_self_argument(self):
        """
        Test that the self argument doesn't fail the check.
        """
        func_node = astroid.extract_node("""
        def test(self, world: SomeClassType, hello: Dict[SomeKeyClass,SomeValueClass]):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_function_with_self_argument_only(self):
        """
        Test that the self argument doesn't fail the check.
        Even if it is the only argument.
        """
        func_node = astroid.extract_node("""
        def test(self):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_type_annotations_with_primitives(self):
        """
        Test that Generic, Alias and Union that contain primitives fails the test.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Union[SomeClassA, int]):  # @
            pass
        """)
        with self.assertAddsMessages(
                pylint.testutils.MessageTest(
                    msg_id="W9003",
                    node=func_node,
                    line=2,
                    col_offset=0,
                    end_line=2,
                    end_col_offset=8
                )
        ):
            self.checker.visit_functiondef(func_node)

    def test_type_annotations_with_no_primitives(self):
        """
        Test that Generic, Alias and Union that contain non primitives passes the test.
        """
        func_node = astroid.extract_node("""
        def test(world: SomeClassType, hello: Union[SomeClassA, SomeClassB]):  # @
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)

    def test_type_annotations_attributes_with_no_primitives(self):
        """
        Test that Generic, Alias and Union that contain non primitives passes the test.
        """
        func_node = astroid.extract_node("""
        def _contains_primitive(self, node: Union[nodes.Name, nodes.Subscript, nodes.Tuple]): #@
            pass
        """)
        with self.assertNoMessages():
            self.checker.visit_functiondef(func_node)
