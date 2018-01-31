#!/usr/bin/env python3
"""Make BALANC3R robot stay upright and move in response to the remote."""

import logging
import time
from ev3dev2.control.GyroBalancer import GyroBalancer, GracefulShutdown
from ev3dev2.sensor.lego import InfraredSensor

# Logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)5s: %(message)s')
log = logging.getLogger(__name__)
log.info("Starting BALANC3R")

# Infrared remote
remote = InfraredSensor()
remote.mode = remote.MODE_IR_REMOTE

# Balance robot
robot = GyroBalancer()
robot.balance()

try:
    while True:
        # Read remote
        button_code = remote.value()

        # Move robot in response to infrared remote
        if button_code == remote.TOP_LEFT_TOP_RIGHT:
            robot.move_forward()
        elif button_code == remote.TOP_LEFT_BOTTOM_RIGHT:
            robot.rotate_right()
        elif button_code == remote.BOTTOM_LEFT_TOP_RIGHT:
            robot.rotate_left()
        elif button_code == remote.BOTTOM_LEFT_BOTTOM_RIGHT:
            robot.move_backward()
        else:
            robot.stop()

        time.sleep(0.5)  # Give CPU a rest

except (GracefulShutdown, Exception) as e:
    log.exception(e)
    # Exit cleanly so that all motors are stopped
    robot.shutdown()

log.info("Exiting BALANC3R")
