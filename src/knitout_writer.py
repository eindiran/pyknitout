"""
"""
from typing import List, Union
from extensions import (PresserMode,
                        set_stitch_num,
                        set_speed_num,
                        set_presser_mode)
from knitout import (Instruction,
                     Direction,
                     StartPosition,
                     Yarn,
                     YarnCarrierMap,
                     Header,
                     format_instruction,
                     knitlp,
                     knitr,
                     tuckmissr,
                     tucklp,
                     inhook,
                     releasehook,
                     outhook,
                     shift)


class KnitoutWriter():
    """
    """
    def __init__(self, carriers: List[str]=[]) -> None:
        self.header = Header(carriers=carriers)
        self.instructions: List[str] = []

    def set_carriers(self, carriers: List[str]) -> None:
        self.header.set_carriers(carriers)

    def set_machine(self, machine: str) -> None:
        self.header.set_machine(machine)

    def set_gauge(self, gauge: Union[str, int]) -> None:
        self.header.set_gauge(gauge)

    def fabric_presser(self, presser_mode: str) -> None:
        self.instructions.append(set_presser_mode(presser_mode))

    def speed(self, speed_num: int) -> None:
        self.instructions.append(set_speed_num(speed_num))

    def stitch(self, stitch_num: int) -> None:
        self.instructions.append(set_stitch_num(stitch_num))

    def knit(self, direction: str, needle: int, carrier: int) -> None:
        self.instructions.append(format_instruction(Instruction.KNIT, direction, needle, carrier))

    def tuck(self, direction: str, needle: int, carrier: int) -> None:
        self.instructions.append(format_instruction(Instruction.TUCK, direction, needle, carrier))

    def miss(self, direction: str, needle: int, carrier: int) -> None:
        self.instructions.append(format_instruction(Instruction.MISS, direction, needle, carrier))

    def inhook(self, carrier: int) -> None:
        self.instructions.append(inhook(carrier))

    def releasehook(self, carrier: int) -> None:
        self.instructions.append(releasehook(carrier))

    def outhook(self, carrier: int) -> None:
        self.instructions.append(outhook(carrier))

    def clear(self) -> None:
        self.instructions = []

    def compile(self) -> str:
        return ''

    def write(self, filename: str) -> None:
        """Write to file."""
        with open(filename, 'w') as outputf:
            compiled_instructions = self.compile()
            outputf.write(compiled_instructions)
