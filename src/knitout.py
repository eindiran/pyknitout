"""
pyknitout/src/knitout.py
Python wrapper for automatically generating valid Knitout files.
Allows you to avoid writing Knitout by hand.
"""
from typing import List, Union
from functools import partial
from enum import Enum


class Instruction(Enum):
    """
    Enum of available instructions in Knitout.
    """
    INHOOK = 'inhook'
    RELEASEHOOK = 'releasehook'
    OUTHOOK = 'outhook'
    KNIT = 'knit'
    TUCK = 'tuck'
    SPLIT = 'split'
    DROP = 'drop'
    AMISS = 'amiss'
    XFER = 'xfer'

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)


class StartPosition(Enum):
    """
    Enum of standard values of starting positions.
    """
    RIGHT = 'right'
    LEFT = 'left'
    CENTER = 'center'
    KEEP = 'keep'

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)


class Yarn():
    """
    Store information about a Yarn in an object.
    Values 'position' and 'name' are mandatory, but additional
    info (wpi, color, and fiber type) can be stores as well.
    These will not be included in the header.
    """
    def __init__(self, name: str,
                 position: Union[str, int],
                 color: str = '',
                 wpi: int = None,
                 fiber: str = '') -> None:
        self.name = name
        self.position = str(position)
        self.key = 'Yarn-{}'.format(position)
        self.color = color
        self.fiber = fiber
        self.wpi = wpi

    def __str__(self) -> str:
        """Overrides __str__ to return `key: name`"""
        return self.key + ': ' + self.name

    def set_wpi(self, wpi: int) -> None:
        """Set the WPI."""
        self.wpi = wpi

    def set_fiber(self, fiber: str) -> None:
        """Set the fiber type."""
        self.fiber = fiber

    def set_color(self, color: str) -> None:
        """Set the yarn color."""
        self.color = color


class YarnCarrierMap():
    """
    A typed dictionary mapping carriers to yarns.
    """
    def __init__(self, carriers: List[str], yarns: List[Yarn]) -> None:
        self.carriers = dict(zip(carriers, yarns))

    def __repr__(self) -> str:
        return str(self.carriers)

    def __contains__(self, carrier: str) -> bool:
        """Allow using `in` operator with YarnCarrierMap."""
        return carrier in self.carriers

    def __getitem__(self, carrier: str) -> Union[Yarn, None]:
        """Allow obj[x]."""
        return self.carriers.get(carrier, None)

    def __setitem__(self, carrier: str, yarn: Union[Yarn, None]) -> None:
        """Allow obj[x] = y."""
        self.carriers[carrier] = yarn

    def __delitem__(self, carrier: str) -> None:
        """Allow del obj[x]."""
        self.carriers.pop(carrier, None)

    def get(self, carrier: str) -> Union[Yarn, None]:
        """Allow obj.get(...) notation."""
        return self.__getitem__(carrier)

    def add(self, carrier: str, yarn: Union[Yarn, None]) -> None:
        """Allow obj.add(x, y) notation as alias to obj[x] = y."""
        self.__setitem__(carrier, yarn)

    def remove(self, carrier: str) -> None:
        """Allow obj.remove(x) notation as alias to del obj[x]."""
        self.__delitem__(carrier)


class Header():
    """
    Encodes a comment header for a Knitout .k file as an object.
    """
    def __init__(self, version: str = '2',
                 carriers: str = '',
                 machine: str = '',
                 gauge: Union[str, int] = '',
                 yarnc: YarnCarrierMap = None,
                 pos: StartPosition = StartPosition.RIGHT) -> None:
        """Initialize a Knitout Header."""
        self.version = version       # version for magic string/shebang line
        lst_carrier = carriers.split(" ")
        self.carriers = lst_carrier  # carriers in front-to-back order
        self.machine = machine       # the model name M of the target machine
        self.gauge = gauge           # the gauge G (in needles/inch) of the target machine
        self.yarnc = yarnc           # yarn to load in carrier C; should be a dict c -> yarn
        self.pos = pos               # position; where to place the operations on the needle bed

    def __repr__(self) -> str:
        """
        Override the default __repr__ to print as a dict of a Header's
        members.
        """
        return 'Header(' + str({'version': self.version,
                                'carriers': self.carriers,
                                'machine': self.machine,
                                'gauge': self.gauge,
                                'yarnc': self.yarnc,
                                'pos': self.pos}) + ')'

    def __str__(self) -> str:
        """Return the value of generate_header()"""
        return self.generate_header()

    def get_carrier_map(self) -> YarnCarrierMap:
        """Get the map of carriers to yarn types."""
        if self.yarnc:
            car_map = self.yarnc
        else:
            car_map = YarnCarrierMap([], [])
        for car in self.carriers:
            if car not in car_map:
                car_map[car] = None
        return car_map

    def get_magic_string(self) -> str:
        """Return the versioned magic string."""
        return ';!knitout-{}'.format(self.version)

    def generate_header(self) -> str:
        """Produce a new copy of a Knitout header."""
        header = self.get_magic_string()
        header += "\n;;Machine: {}\n".format(self.machine)
        header += ";;Gauge: {}\n".format(self.gauge)
        if self.yarnc:
            for car, yarn in self.yarnc.carriers.items():
                header += ";;Yarn-{}: {}\n".format(car, yarn)
        header += ";;Carriers:"
        for car in self.carriers:
            header += " " + car
        header += "\n;;Position: {}\n\n".format(self.pos)
        return header


def _format_instruction(instruction: str, cdir: str, num: str, hook: str) -> str:
    """Format a single Knitout instruction."""
    return instruction + " " + cdir + " f" + num + " " + hook + "\n"


def _loop(instr: str, loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a set of Knitout instructions based on a set of numbers in a loop."""
    out_str = ""
    for num in loop_nums:
        out_str += _format_instruction(instr, curr_dir, str(num), str(curr_hook))
    return out_str


def knitlp(loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a knit loop."""
    return partial(_loop, Instruction.KNIT.value)(loop_nums, curr_dir, curr_hook)


def tucklp(loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a tuck loop."""
    return partial(_loop, Instruction.TUCK.value)(loop_nums, curr_dir, curr_hook)
