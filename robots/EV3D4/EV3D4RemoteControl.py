#!/usr/bin/env python3

import logging
import sys
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MediumMotor
from ev3dev2.control.rc_tank import RemoteControlledTank


class EV3D4RemoteControlled(RemoteControlledTank):

    def __init__(self, medium_motor=OUTPUT_A, left_motor=OUTPUT_C, right_motor=OUTPUT_B):
        RemoteControlledTank.__init__(self, left_motor, right_motor)
        self.medium_motor = MediumMotor(medium_motor)
        self.medium_motor.reset()


if __name__ == '__main__':

    # Change level to logging.INFO to make less chatty
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)5s %(filename)s:%(lineno)5s - %(funcName)25s(): %(message)s")
    log = logging.getLogger(__name__)

    # Color the errors and warnings in red
    logging.addLevelName(logging.ERROR, "\033[91m  %s\033[0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))

    log.info("Starting EV3D4")
    ev3d4 = EV3D4RemoteControlled()
    ev3d4.main()
    log.info("Exiting EV3D4")
