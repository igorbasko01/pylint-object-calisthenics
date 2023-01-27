"""Unit tests module for PackageSize checker"""
import astroid
import pylint.testutils

from astroid.builder import AstroidBuilder
from object_calisthenics.checkers.package_size import PackageSize


class TestPackageSize(pylint.testutils.CheckerTestCase):
    """Test case for PackageSize checker"""
    CHECKER_CLASS = PackageSize

    def test_package_has_too_much_files(self):
        module = AstroidBuilder().file_build('../object_calisthenics/checkers/__init__.py')
        self.assertNoMessages()