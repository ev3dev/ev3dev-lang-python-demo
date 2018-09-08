#!/usr/bin/env python3
"""
Move robot in a square path using the Gyro sensor.

This script is a simple demonstration of turning using the Gyro sensor.
"""

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import GyroSensor


motor_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
gyro = GyroSensor()
gyro.mode = GyroSensor.MODE_GYRO_ANG

for i in range(4):

    # Move robot forward for 3 seconds
    motor_pair.on_for_seconds(steering=0, speed=50, seconds=3)

    # Spin robot to the left
    motor_pair.on(steering=-100, speed=5)

    # Wait until angle changed by 90 degrees
    gyro.wait_until_angle_changed_by(90)

    # Stop motors
    motor_pair.off()
