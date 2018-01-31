#!/usr/bin/env python3
"""Make BALANC3R robot stay upright and move in a pattern."""

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
    # Wait for top left button on remote to be pressed
    button_code = remote.value()
    while button_code != remote.TOP_LEFT:
        button_code = remote.value()
        time.sleep(0.5)  # Give CPU a rest

    # Move robot in a simple pattern
    robot.rotate_left(seconds=3)
    robot.rotate_right(seconds=3)
    robot.move_forward(seconds=3)
    robot.move_backward(seconds=3)

    # Wait for user to terminate program
    while True:
        time.sleep(0.5)

except (GracefulShutdown, Exception) as e:
    log.exception(e)
    # Exit cleanly so that all motors are stopped
    robot.shutdown()

log.info("Exiting BALANC3R")
