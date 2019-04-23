"""
pyknitout/test/wrapper_tests.py
Tests for the pyknitout Python Knitout compiler.
"""
import unittest
from knitout import (StartPosition, Instruction,
                     Yarn, Header, knitlp, tucklp)


class TestHeaderGeneration(unittest.TestCase):
    """Test the generation of a Knitout header."""
    def test_header():
        """
        Get a header object and compare the generated
        string to the real Knitout we expect.
        """

    def test_single_yarn():
        """Test that we can create a header with a single yarn."""

    def test_multiple_yarn():
        """Test that we can create a header with multiple yarns."""

    def test_yarn_fail():
        """Test that a header fails to generate when no yarns are given."""

    def test_magic_string():
        """
        Check that a header contains a magic string.
        """
        yarn = Yarn(name="30-70 Gold Belt", position=1)
        st_pos = StartPosition.CENTER
        header = str(Header(version='2.0', carriers='0 1 2 3', machine='DE-FN1922',
                        gauge=15, yarnc=yarn, pos=st_pos))




    def test_default_version():
        """Check that we can generate a header without specifying the version of Knitout."""

    def test_magic_string_override():
        """Check that we are able to override the magic string in a header."""



def test_header():
    """
    Test the production of Knitout headers.
    """
    yarn = {"1": "50-50 Rust", "3": "100:0 Magic Blonde"}
    header_obj = Header(version="2.0", carriers="0 1 2 3", machine="SWG091N2",
                        gauge="15", yarnc=yarn, pos="Right")
    header_cpy = header_obj.generate_header()
    test_str = ";!knitout-2.0\n;;Machine: SWG091N2\n;;Gauge: 15\n;;Yarn-1: 50-50 Rust\n"
    test_str += ";;Yarn-3: 100:0 Magic Blonde\n;;Carriers: 0 1 2 3\n;;Position: Right\n\n"
    assert header_cpy == test_str
    print(header_cpy)


def test_knitlp():
    """
    Test the generation of a knit loop.
    """
    knit_range = reversed(range(1, 11))
    print(knitlp(knit_range, "-", "5"))
    knit_range = range(1, 11)
    print(knitlp(knit_range, "+", "5"))


def test_tucklp():
    """
    Test the generation of a tuck loop.
    """
    knit_range = reversed(range(2, 12, 2))
    print(tucklp(knit_range, "-", "5"))
    knit_range = range(1, 11, 2)
    print(tucklp(knit_range, "+", "5"))


def run_all_tests():
    """
    Run all tests in panel.
    """
    test_header()
    test_knitlp()
    test_tucklp()


if __name__ == "__main__":
    run_all_tests()
