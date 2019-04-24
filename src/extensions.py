"""
pyknitout/src/extensions.py
Support for Knitout extensions:
    x-stitch-number
    x-speed-number
    x-presser-mode
More info here: https://textiles-lab.github.io/knitout/extensions.html
"""
from enum import Enum


class PresserMode(Enum):
    """
    Enum of the fabric presser mode extension values.
    Part of the supported Knitout extensions.
    Default: OFF
    """
    OFF = 'off'     # No fabric presser
    AUTO = 'auto'   # Fabric presser on passes with only front or only back stitches
    ON = 'on'       # Break passes so that fabric presser can always be used

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)


def set_stitch_num(stitch_num: int) -> str:
    """Set the stitch number. Part of the supported Knitout extensions."""
    return 'x-stitch-number {}'.format(stitch_num)


def set_speed_num(speed_num: int) -> str:
    """
    Set the speed number. Part of the supported Knitout extensions.
    Valid speed numbers are positive integers in the range 0 - 15
    Raises ValueError
    """
    if 0 <= speed_num <= 15:
        return 'x-speed-number {}'.format(speed_num)
    else:
        raise ValueError('int speed_num (val: {}) must in range 0-15.'.format(speed_num))


def set_presser_mode(presser_mode: PresserMode) -> str:
    """
    Set the fabric presser mode. Part of the supported Knitout extensions.
    By default, if set_presser_mode is not called, the mode will be set to PresserMode.OFF
    """
    return 'x-presser-mode {}'.format(presser_mode)
