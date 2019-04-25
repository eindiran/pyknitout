"""
pyknitout/test/test_wrapper.py
Tests for the main pyknitout wrapper.
"""
import unittest
from knitout import (StartPosition, Instruction,
                     Yarn, YarnCarrierMap,
                     Header, knitlp, tucklp)


class TestTucklp(unittest.TestCase):
    """Test the tucklp() tuck instuction loop."""

    def test_tucklp_forward(self):
        """Test the forward tucklp loop."""
        knit_range = reversed(range(2, 12, 2))
        expected_str = 'tuck - f10 5\n' + \
                       'tuck - f8 5\n' + \
                       'tuck - f6 5\n' + \
                       'tuck - f4 5\n' + \
                       'tuck - f2 5\n\n'
        self.assertEqual(expected_str, tucklp(knit_range, "-", "5"))

    def test_tucklp_backward(self):
        """Test the backward tucklp loop."""
        knit_range = range(1, 11, 2)
        expected_str = 'tuck + f1 5\n' + \
                       'tuck + f3 5\n' + \
                       'tuck + f5 5\n' + \
                       'tuck + f7 5\n' + \
                       'tuck + f9 5\n\n'
        self.assertEqual(expected_str, tucklp(knit_range, "+", "5"))


class TestHeaderGeneration(unittest.TestCase):
    """Test the generation of a Knitout header."""
    def test_header(self):
        """
        Get a header object and compare the generated
        string to the real Knitout we expect.
        """
        yarns = [Yarn(name='50-50 Rust'), Yarn(name='100:0 Magic Blonde')]
        positions = [1, 3]
        yarnc = YarnCarrierMap(positions, yarns)
        st_pos = StartPosition.RIGHT
        header = str(Header(version='2.0', carriers='0 1 2 3 4 5', machine='AS22-SEWSTAR',
                            gauge=10, yarnc=yarnc, pos=st_pos))
        expected_str = ';!knitout-2.0\n;;Machine: AS22-SEWSTAR\n;;Gauge: 10\n' + \
            ';;Yarn-1: 50-50 Rust\n;;Yarn-3: 100:0 Magic Blonde\n;;Carriers: 0 1 2 3 4 5\n' + \
            ';;Position: right\n\n'
        self.assertEqual(expected_str, header)

    def test_single_yarn(self):
        """Test that we can create a header with a single yarn."""
        yarns = [Yarn(name="50-50 Silver Silk")]
        positions = [1]
        yarnc = YarnCarrierMap(positions, yarns)
        st_pos = StartPosition.CENTER
        header = str(Header(version='2.0', carriers='0 1 2 3', machine='DE-FN1922',
                            gauge=15, yarnc=yarnc, pos=st_pos))
        expected_str = ';!knitout-2.0\n;;Machine: DE-FN1922\n;;Gauge: 15\n' + \
            ';;Yarn-1: 50-50 Silver Silk\n;;Carriers: 0 1 2 3\n;;Position: center\n\n'
        self.assertEqual(expected_str, header)

    def test_multiple_yarn(self):
        """Test that we can create a header with multiple yarns."""
        yarns = [Yarn(name='30-70 Gold Belt'), Yarn(name='Ashkani Blue')]
        positions = [1, 7]
        yarnc = YarnCarrierMap(yarns, positions)
        st_pos = StartPosition.RIGHT
        header = str(Header(version='1.75', carriers='0 1 2 3 4 5 6 7', machine='DALENDA-70S',
                            gauge=22, yarnc=yarnc, pos=st_pos))
        expected_str = ';!knitout-1.75\n;;Machine: DALENDA-70S\n;;Gauge: 22\n' + \
            ';;Yarn-30-70 Gold Belt: 1\n;;Yarn-Ashkani Blue: 7\n;;Carriers: 0 1 2 3 4 5 6 7\n' + \
            ';;Position: right\n\n'
        self.assertEqual(expected_str, header)

    def test_empty_yarn(self):
        """Test that we can create a header with no yarns in the yarn list."""
        yarns = []
        positions = []
        st_pos = StartPosition.LEFT
        yarnc = YarnCarrierMap(yarns, positions)
        header = str(Header(version='2.0', carriers='0 1 2 3', machine='Q-SEW-MASTER-22', gauge=12,
                            yarnc=yarnc, pos=st_pos))
        expected_str = ';!knitout-2.0\n;;Machine: Q-SEW-MASTER-22\n;;Gauge: 12\n' + \
            ';;Carriers: 0 1 2 3\n;;Position: left\n\n'
        self.assertEqual(expected_str, header)

    def test_magic_string(self):
        """
        Check that a header contains a magic string.
        """
        yarns = [Yarn(name="30-70 Gold Belt")]
        positions = [1]
        yarnc = YarnCarrierMap(positions, yarns)
        st_pos = StartPosition.CENTER
        header = str(Header(version='2.0', carriers='0 1 2 3', machine='DE-FN1922',
                            gauge=15, yarnc=yarnc, pos=st_pos))
        magic_str = header.split('\n')[0]
        self.assertEqual(';!knitout-2.0', magic_str)

    def test_magic_string_override(self):
        """Check that we are able to override the magic string in a header."""
        yarns = [Yarn(name="60:40 Red-Yellow Autumn")]
        positions = [1]
        yarnc = YarnCarrierMap(positions, yarns)
        st_pos = StartPosition.LEFT
        header = str(Header(version='0.1', carriers='0 1 2 3', machine='DE-FN1922',
                            gauge=15, yarnc=yarnc, pos=st_pos))
        magic_str = header.split('\n')[0]
        self.assertEqual(';!knitout-0.1', magic_str)


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



if __name__ == "__main__":
    unittest.main()
