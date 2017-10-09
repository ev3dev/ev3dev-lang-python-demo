#!/usr/bin/env python3

"""
This program is used to measure the white center of your rubiks cube to
calibrate the color sensor as to what "white" is. Place the white center
of your 3x3x3 rubiks cube facing up and run this program. It will only
scan the white center cube and will then write the red/green/blue values
to a max_rgb.txt file. When mindcuber.py runs it will look for the
max_rgb.txt file and if it exists will read in the values to calibrate
the color sensor.

If you move to a different room with different lighting it is a good idea
to run this program again.
"""

from mindcuber import MindCuber
import logging
import sys


# logging.basicConfig(filename='rubiks.log',
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)12s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))

mcube = MindCuber()

try:
    mcube.wait_for_cube_insert()

    # Push the cube to the right so that it is in the expected
    # position when we begin scanning
    mcube.flipper_hold_cube(100)
    mcube.flipper_away(100)

    # Scan the middle square
    mcube.colorarm_middle()
    mcube.color_sensor.calibrate_white()

    with open('max_rgb.txt', 'w') as fh:
        fh.write("red %s\n" % mcube.color_sensor.red_max)
        fh.write("green %s\n" % mcube.color_sensor.green_max)
        fh.write("blue %s\n" % mcube.color_sensor.blue_max)

    mcube.colorarm_remove()
    mcube.shutdown_robot()

except Exception as e:
    log.exception(e)
    mcube.shutdown_robot()
    sys.exit(1)
