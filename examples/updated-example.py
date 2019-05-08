from knitout import KnitoutWriter

k = KnitoutWriter()

k.set_carriers([str(x) for x in range(1, 10)])
k.set_machine('SWGXYZ')
k.set_gauge(15)

height = 10
width = 10
carrier = 6
k.fabric_presser('auto')
k.inhook(carrier)

for s in range(width, -1, -1):
    if s % 2 == 0:
        k.tuck('-', s, carrier)
    else:
        k.miss('-', s, carrier)

for s in range(1, width):
    if s % 2 != 0:
        k.tuck('+', s, carrier)
    else:
        k.miss('+', s, carrier)

k.releasehook(carrier)

for h in range(height):
    for s in range(width, -1, -1):
        k.knit('-', s, carrier)
    for s in range(1, width):
        k.knit('+', s, carrier)

"""
for _ in range(height):
    k.knitr(width, '-', carrier)
    k.knitr(width, '+', carrier)
"""

k.outhook(carrier)

k.done()
