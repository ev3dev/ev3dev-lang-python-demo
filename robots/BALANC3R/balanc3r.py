#!/usr/bin/env python3
"""Make BALANC3R robot stay upright and move in response to the remote."""

import logging
from ev3dev.control.GyroBalancer import GyroBalancer
from ev3dev.motor import OUTPUT_A, OUTPUT_D


class BALANC3R(GyroBalancer):
    """
    Laurens Valk's BALANC3R.

    http://robotsquare.com/2014/07/01/tutorial-ev3-self-balancing-robot/
    """

    def __init__(self):
        """Create BALANC3R."""
        super().__init__(gain_gyro_angle=1700,
                         gain_gyro_rate=120,
                         gain_motor_angle=7,
                         gain_motor_angular_speed=9,
                         gain_motor_angle_error_accumulated=3,
                         left_motor_port=OUTPUT_D,
                         right_motor_port=OUTPUT_A)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)5s: %(message)s')
    log = logging.getLogger(__name__)

    log.info("Starting BALANC3R")
    robot = BALANC3R()
    robot.main()
    log.info("Exiting BALANC3R")
