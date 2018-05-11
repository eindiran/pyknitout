"""
Use Python code to automatically generate valid Knitout files.
Allows you to avoid writing Knitout by hand.
"""
from typing import Dict, List, Union
from collections import OrderedDict
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


class Header():
    """
    Encodes a comment header for a Knitout .k file.
    """
    def __init__(self, version="2", carriers="", machine="", gauge="",
                 yarnc=dict(), pos="") -> None:
        """Initialize a Knitout Header."""
        self.version = version    # version for magic string/shebang line
        carriers = carriers.split(" ")
        self.carriers = carriers  # carriers in front-to-back order
        self.machine = machine    # the model name M of the target machine
        self.gauge = gauge        # the gauge G (in needles/inch) of the target machine
        self.yarnc = yarnc        # yarn to load in carrier C; should be a dict c -> yarn
        self.pos = pos            # position; where to place the operations on the needle bed
#                                 # Left, Center, Right, and Keep are standard values

    def get_carrier_map(self) -> Dict[str, Union[str, None]]:
        """Get the map of carriers to yarn types."""
        car_map = OrderedDict()  # type: Dict[str, Union[str, None]]
        for car in self.carriers:
            if car in self.yarnc:
                car_map[car] = self.yarnc[car]
            else:
                car_map[car] = None
        return car_map

    def generate_header(self) -> str:
        """Produce a new copy of a Knitout header."""
        header = ";!knitout-" + self.version + "\n"
        header += ";;Machine: " + self.machine + "\n"
        header += ";;Gauge: " + self.gauge + "\n"
        car_map = self.get_carrier_map()
        for car, yarn in car_map.items():
            if yarn:
                header += ";;Yarn-" + car + ": " + yarn + "\n"
        header += ";;Carriers:"
        for car in self.carriers:
            header += " " + car
        header += "\n"
        header += ";;Position: " + self.pos + "\n\n"
        return header


def format_instruction(instruction: str, cdir: str, num: str, hook: str) -> str:
    """Format a single Knitout instruction."""
    return instruction + " " + cdir + " f" + num + " " + hook + "\n"


def loop(instr: str, loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a set of Knitout instructions based on a set of numbers in a loop."""
    out_str = ""
    for num in loop_nums:
        out_str += format_instruction(instr, curr_dir, str(num), str(curr_hook))
    return out_str


def knitlp(loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a knit loop."""
    return partial(loop, Instruction.KNIT.value)(loop_nums, curr_dir, curr_hook)


def tucklp(loop_nums: List[int], curr_dir: str, curr_hook: int) -> str:
    """Generate a tuck loop."""
    return partial(loop, Instruction.TUCK.value)(loop_nums, curr_dir, curr_hook)
