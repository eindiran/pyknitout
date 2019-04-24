"""
pyknitout/test/test_extensions.py
Tests for the Knitout extensions supported in pyknitout.
More info here: https://textiles-lab.github.io/knitout/extensions.html
"""
import unittest
from extensions import (PresserMode, set_stitch_num,
                        set_speed_num, set_presser_mode)


class PresserModeExtensionTest(unittest.TestCase):
    """Test the presser mode Knitout extension."""

    def test_set_with_str(self):
        """Test that we can use a string to set the presser mode."""
        presser_modes = ['auto', 'off', 'on']
        for presser_mode in presser_modes:
            expected_output = 'x-presser-mode {}'.format(presser_mode)
            self.assertEqual(set_presser_mode(presser_mode), expected_output)

    def test_set_with_enum(self):
        """Test that we can use the PresserMode enum to set a presser mode."""
        presser_modes = [PresserMode.AUTO, PresserMode.OFF, PresserMode.ON]
        presser_mode_strs = ['auto', 'off', 'on']
        for pme, pms in zip(presser_modes, presser_mode_strs):
            expected_output = 'x-presser-mode {}'.format(pms)
            self.assertEqual(set_presser_mode(pme), expected_output)

    def test_raises_value_error(self):
        """Test that a ValueError is raised if set_presser_mode() is passed an invalid string."""
        junk_strings = ['bad string', 'auuto', '', 'invalid-string']
        for js in junk_strings:
            with self.assertRaises(ValueError):
                set_presser_mode(js)


class StitchNumberExtensionTest(unittest.TestCase):
    """Test the stitch number Knitout extension."""

    def test_set_stitch_num(self):
        """Test set_stitch_num()."""
        for stitch in range(-5, 100):
            expected_output = 'x-stitch-number {}'.format(stitch)
            self.assertEqual(set_stitch_num(stitch), expected_output)


class SpeedNumberExtensionTest(unittest.TestCase):
    """Test the speed number Knitout extension."""

    def test_set_speed_number(self):
        """Test set_speed_number()."""
        for speed in range(16):
            expected_output = 'x-speed-number {}'.format(speed)
            self.assertEqual(set_speed_num(speed), expected_output)

    def test_raises_value_error(self):
        """Test that ValueError is raised when speed_num is outside range [0 - 15]."""
        invalid_speeds = [-100, -7, -2, -1, 16, 17, 100, 1026]
        for speed in invalid_speeds:
            with self.assertRaises(ValueError):
                set_speed_num(speed)


if __name__ == '__main__':
        unittest.main()
