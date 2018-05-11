"""
Tests for the Python Knitout compiler.
"""
from knitout import Header, knitlp, tucklp


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
