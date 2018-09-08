#!/usr/bin/env python3
"""
Move robot in a square path without using the Gyro sensor.

This script is a simple demonstration of moving forward and turning.
"""

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C

motor_pair = MoveSteering(OUTPUT_B, OUTPUT_C)

for i in range(4):

    # Move robot forward for 3 seconds
    motor_pair.on_for_seconds(steering=0, speed=50, seconds=3)

    # Turn robot left 90 degrees (adjust rotations for your particular robot)
    motor_pair.on_for_rotations(steering=-100, speed=5, rotations=0.5)
