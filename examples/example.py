"""
example.py -- recreate the example from the Knitout specification page.
"""
from knitout import Header, knitlp, tucklp


yarn = {"1": "50-50 Rust"}
header_obj = Header(version="2.0", carriers="1 2 3 4 5 6 7 8 9 10", machine="SWG091N2",
                    gauge="15", yarnc=yarn, pos="Right")
with open("simple.knitout", "w") as o:
    o.write(header_obj.generate_header())
    # header done, start with basic knit loop
    o.write(knitlp(reversed(range(1, 11)), "-", "5"))
    o.write(knitlp(range(1, 11), "+", "5"))
    o.write(tucklp(reversed(range(2, 12, 2)), "-", "5"))
    o.write(tucklp(range(1, 11, 2), "+", "5"))
