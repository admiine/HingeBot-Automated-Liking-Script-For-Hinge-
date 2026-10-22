"""Helper for creating the two template images.

Usage:
  python make_template.py shot                      # saves screen.png from the emulator
  python make_template.py crop NAME X1 Y1 X2 Y2     # crops screen.png into NAME.png
"""
import sys

import uiautomator2 as u2
from PIL import Image

DEVICE = "127.0.0.1:16384"

if len(sys.argv) >= 2 and sys.argv[1] == "shot":
    u2.connect(DEVICE).screenshot("screen.png")
    print("saved screen.png")
elif len(sys.argv) == 7 and sys.argv[1] == "crop":
    name = sys.argv[2]
    box = tuple(int(v) for v in sys.argv[3:7])
    Image.open("screen.png").crop(box).save(f"{name}.png")
    print(f"saved {name}.png from box {box}")
else:
    print(__doc__)
