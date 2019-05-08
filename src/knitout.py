"""
pyknitout/src/knitout.py
Python wrapper for automatically generating valid Knitout files.
Allows you to avoid writing Knitout by hand.
"""
from typing import Dict, List, Union
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
    MISS = 'miss'
    XFER = 'xfer'

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.value


class Direction(Enum):
    """
    Enum of directions: '-' and '+'.
    """
    FORWARD = '+'
    BACKWARD = '-'

    def __repr__(self):
        return '<{}.{}>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.value



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

    def __str__(self):
        return '{}'.format(self.value)


class Yarn():
    """
    Store information about a Yarn in an object.
    The value 'name' is mandatory, but additional
    info (wpi, color, and fiber type) can be stored
    optionally as well. Optional info will not be
    included in the header.
    """
    def __init__(self, name: str,
                 # position: Union[str, int],
                 color: str = '',
                 wpi: int = None,
                 fiber: str = '') -> None:
        self.name = name
        # self.position = str(position)
        # self.key = 'Yarn-{}'.format(position)
        self.color = color
        self.fiber = fiber
        self.wpi = wpi

    def __str__(self) -> str:
        """Overrides __str__ to return `key: name`"""
        # return self.key + ': ' + self.name
        return self.name

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

    def __str__(self) -> str:
        items = []
        for key, value in self.carriers.items():
            items.append(';;Yarn-{}: {}\n'.format(key, value))
        return ''.join(items)

    def __contains__(self, carrier: str) -> bool:
        """Allow using `in` operator with YarnCarrierMap."""
        return carrier in self.carriers

    def __getitem__(self, carrier: str) -> Union[Yarn, None]:
        """Allow obj[x]."""
        return self.carriers.get(carrier, None)

    def __setitem__(self, carrier: str, yarn: Union[Yarn, None]) -> None:
        """Allow obj[x] = y."""
        if yarn:
            self.carriers[carrier] = yarn
        else:
            raise TypeError('yarn was None, but should be of type Yarn')

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
                 carriers: List[str] = [],
                 machine: str = '',
                 gauge: Union[str, int] = '',
                 yarnc: YarnCarrierMap = None,
                 pos: StartPosition = StartPosition.RIGHT) -> None:
        """Initialize a Knitout Header."""
        self.version = version           # version for magic string/shebang line
        self.carriers = carriers         # carriers in front-to-back order
        self.machine = machine           # the model name M of the target machine
        self.gauge = gauge               # the gauge G (in needles/inch) of the target machine
        self.yarnc = yarnc               # yarn to load in carrier C; should be a dict c -> yarn
        self.pos = pos                   # starting position
        self.other: Dict[str, str] = {}  # Other comments; add dynamically with add_header()

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
                                'pos': self.pos,
                                'other': self.other}) + ')'

    def __str__(self) -> str:
        """Return the value of generate_header()"""
        return self.generate_header()

    def add_header(self, comment_k: str, comment_v: Union[str, int]) -> None:
        """Add a new line to the header."""
        self.other[comment_k] = str(comment_v)

    def set_carriers(self, carriers: List[str]) -> None:
        """Set the carrier list."""
        self.carriers = carriers

    def set_machine(self, machine: str) -> None:
        """Set the machine."""
        self.machine = machine

    def set_gauge(self, gauge: Union[str, int]) -> None:
        """Set the gauge."""
        self.gauge = str(gauge)

    def set_position(self, pos: StartPosition) -> None:
        """Set the starting position."""
        self.pos = pos

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
        """
        Produce a new copy of a Knitout header.
        """
        header = self.get_magic_string()
        if self.machine:
            header += "\n;;Machine: {}\n".format(self.machine)
        if self.gauge:
            header += ";;Gauge: {}\n".format(self.gauge)
        if self.yarnc:
            for car, yarn in self.yarnc.carriers.items():
                header += ";;Yarn-{}: {}\n".format(car, yarn)
        if self.carriers:
            header += ";;Carriers:"
            for car in self.carriers:
                header += " " + car
        for comment_k, comment_v in self.other.items():
            header += ";;{}: {}\n".format(comment_k, comment_v)
        header += ";;Position: {}\n\n".format(self.pos)
        return header


def format_instruction(instruction: Instruction, cdir: Direction, num: Union[str, int],
                        carrier: Union[str, int]) -> str:
    """Format a single Knitout instruction."""
    return '{} {} f{} {}\n'.format(instruction, cdir, num, carrier)


def _loop(instr: Instruction, loop_nums: List[int], cdir: Direction,
          carrier: Union[str, int]) -> str:
    """Generate a set of Knitout instructions based on a set of numbers in a loop."""
    out_str = ""
    for num in loop_nums:
        out_str += format_instruction(instr, cdir, str(num), str(carrier))
    return out_str


def knitlp(loop_nums: List[int], cdir: str, carrier: int) -> str:
    """Generate a knit loop from a list of needle numbers."""
    return partial(_loop, Instruction.KNIT.value)(loop_nums, cdir, carrier)


def knitr(width: int, cdir: str, carrier: int) -> str:
    """Generate a unidirectional knit loop from a width."""
    if cdir is '-':
        return knitlp(list(range(width, -1, -1)), '-', carrier)
    elif cdir is '+':
        return knitlp(list(range(1, width)), '+', carrier)
    else:
        raise ValueError('Direction {} is not either \'+\' or \'-\'')


def tuckmissr(width: int, cdir: str, carrier: int) -> str:
    """Generate an alternating tuck/miss loop in one direction."""
    loop_instructions = []
    if cdir is '-':
        for s in range(width, -1, -1):
            if s % 2 == 0:
                loop_instructions.append(format_instruction(Instruction.TUCK,
                                                             Direction.BACKWARD,
                                                             str(s),
                                                             carrier))
            else:
                loop_instructions.append(format_instruction(Instruction.MISS,
                                                             Direction.BACKWARD,
                                                             str(s),
                                                             carrier))
    elif cdir is '+':
        for s in range(width):
            if s % 2 != 0:
                loop_instructions.append(format_instruction(Instruction.TUCK,
                                                             Direction.FORWARD,
                                                             str(s),
                                                             carrier))
            else:
                loop_instructions.append(format_instruction(Instruction.MISS,
                                                             Direction.FORWARD,
                                                             str(s),
                                                             carrier))
    else:
        raise ValueError('Direction {} is not either \'+\' or \'-\'')
    return ''.join(loop_instructions)


def tucklp(loop_nums: List[int], cdir: str, carrier: int) -> str:
    """Generate a tuck loop."""
    return partial(_loop, Instruction.TUCK.value)(loop_nums, cdir, carrier)


def shift(dir: str, from_bed: str, to_bed: str, carriers: List[str]) -> str:
    """"""
    pass


def inhook(carrier: int) -> str:
    return '{} {}\n'.format(Instruction.INHOOK, carrier)


def releasehook(carrier: int) -> str:
    return '{} {}\n'.format(Instruction.RELEASEHOOK, carrier)


def outhook(carrier: int) -> str:
    return '{} {}'.format(Instruction.OUTHOOK, carrier)
